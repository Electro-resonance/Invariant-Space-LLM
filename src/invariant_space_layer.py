"""Dynamic Invariant Space Layer: minimal PyTorch prototype.

Author: Martin Timms
Repository: Invariant-Space-LLM
Paper: "Inversion Is All You Need: Dynamic Invariant Spaces for Transformer Language Models"

MIT License - code example.
Copyright (c) 2026 Martin Timms.

This file is an illustrative research snippet only. It is not production software,
not a safety-tested model component, and not a guarantee of any particular
performance, legal suitability, or fitness for purpose. The code is provided
"as is" under the MIT portion of the repository LICENSE, without warranties
or guarantees of any kind.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class InvariantSpaceState:
    """Persistent state for a Dynamic Invariant Space layer.

    phase_memory shape: [batch, phase_dim]
    """

    phase_memory: torch.Tensor


class InvariantSpaceLayer(nn.Module):
    """A lightweight dynamic invariant workspace for transformer hidden states.

    Args:
        d_model: transformer hidden size.
        phase_dim: number of oscillator phase channels, often 12 for OpenGML-inspired geometry.
        hidden_dim: internal nested convergence width.
        coupling_steps: number of oscillator update iterations.
        memory_decay: decay factor for persistent phase memory.
        residual_scale: initial scale for residual correction.

    Input:
        x: [batch, seq, d_model]
        state: optional InvariantSpaceState

    Output:
        y: [batch, seq, d_model]
        new_state: InvariantSpaceState
        diagnostics: dict of scalar tensors
    """

    def __init__(
        self,
        d_model: int,
        phase_dim: int = 12,
        hidden_dim: int = 64,
        coupling_steps: int = 2,
        memory_decay: float = 0.95,
        residual_scale: float = 0.05,
    ) -> None:
        super().__init__()
        if phase_dim < 3:
            raise ValueError("phase_dim should be at least 3")
        self.d_model = d_model
        self.phase_dim = phase_dim
        self.hidden_dim = hidden_dim
        self.coupling_steps = coupling_steps
        self.memory_decay = memory_decay

        self.to_phase = nn.Linear(d_model, phase_dim)
        self.drive = nn.Linear(d_model, phase_dim)

        # Trainable ring and global coupling. Keep small initial values for stability.
        self.ring_coupling = nn.Parameter(torch.randn(phase_dim) * 0.02)
        self.global_coupling = nn.Parameter(torch.tensor(0.03))
        self.prime_mod = nn.Parameter(torch.linspace(2, 43, phase_dim).float(), requires_grad=False)

        # Nested convergence: phase sin/cos features -> hidden -> smaller hidden -> 1 convergence scalar -> d_model.
        self.nest1 = nn.Linear(phase_dim * 2, hidden_dim)
        self.nest2 = nn.Linear(hidden_dim, max(8, hidden_dim // 3))
        self.nest3 = nn.Linear(max(8, hidden_dim // 3), 1)
        self.from_invariant = nn.Linear(1 + hidden_dim + phase_dim * 2, d_model)

        self.residual_scale = nn.Parameter(torch.tensor(float(residual_scale)))
        self.norm = nn.LayerNorm(d_model)

    def initial_state(self, batch_size: int, device: torch.device, dtype: torch.dtype) -> InvariantSpaceState:
        return InvariantSpaceState(phase_memory=torch.zeros(batch_size, self.phase_dim, device=device, dtype=dtype))

    @staticmethod
    def _wrap_phase(phi: torch.Tensor) -> torch.Tensor:
        """Wrap phase to [-pi, pi]."""
        return torch.atan2(torch.sin(phi), torch.cos(phi))

    def forward(
        self,
        x: torch.Tensor,
        state: Optional[InvariantSpaceState] = None,
    ) -> Tuple[torch.Tensor, InvariantSpaceState, Dict[str, torch.Tensor]]:
        if x.ndim != 3:
            raise ValueError("Expected x with shape [batch, seq, d_model]")

        b, s, _ = x.shape
        x_norm = self.norm(x)
        if state is None:
            state = self.initial_state(b, x.device, x.dtype)

        # Phase drive per token plus persistent memory broadcast across sequence.
        phase = torch.tanh(self.to_phase(x_norm)) * torch.pi
        drive = torch.tanh(self.drive(x_norm))
        memory = state.phase_memory[:, None, :]
        phi = phase + memory

        # Simple oscillator dynamics with ring neighbours, global mean coupling, and prime modulation.
        prime = self.prime_mod.to(device=x.device, dtype=x.dtype)[None, None, :]
        for _ in range(self.coupling_steps):
            left = torch.roll(phi, shifts=1, dims=-1)
            right = torch.roll(phi, shifts=-1, dims=-1)
            ring = torch.sin(left - phi) + torch.sin(right - phi)
            global_phase = torch.atan2(torch.sin(phi).mean(dim=-1, keepdim=True), torch.cos(phi).mean(dim=-1, keepdim=True))
            glob = torch.sin(global_phase - phi)
            prime_term = 0.01 * torch.sin(prime * phi)
            phi = self._wrap_phase(phi + drive * 0.05 + self.ring_coupling * ring + self.global_coupling * glob + prime_term)

        features = torch.cat([torch.sin(phi), torch.cos(phi)], dim=-1)
        h1 = F.gelu(self.nest1(features))
        h2 = F.gelu(self.nest2(h1))
        invariant_state = torch.tanh(self.nest3(h2))
        fused = torch.cat([invariant_state, h1, features], dim=-1)
        correction = self.from_invariant(fused)

        y = x + torch.tanh(self.residual_scale) * correction

        # Update persistent memory using sequence-average phase.
        seq_phase = torch.atan2(torch.sin(phi).mean(dim=1), torch.cos(phi).mean(dim=1))
        new_memory = self.memory_decay * state.phase_memory + (1.0 - self.memory_decay) * seq_phase
        new_memory = self._wrap_phase(new_memory.detach())
        new_state = InvariantSpaceState(phase_memory=new_memory)

        # Kuramoto-style order parameter: 1 = coherent, 0 = incoherent.
        order_complex_real = torch.cos(phi).mean(dim=-1)
        order_complex_imag = torch.sin(phi).mean(dim=-1)
        order_r = torch.sqrt(order_complex_real**2 + order_complex_imag**2)
        phase_entropy_proxy = 1.0 - order_r

        diagnostics = {
            "invariant_order_r": order_r.mean(),
            "invariant_phase_entropy_proxy": phase_entropy_proxy.mean(),
            "invariant_abs": invariant_state.abs().mean(),
            "invariant_residual_scale": torch.tanh(self.residual_scale).detach(),
        }
        return y, new_state, diagnostics


def invariant_regularization(diagnostics: Dict[str, torch.Tensor], target_r: float = 0.55, weight: float = 0.01) -> torch.Tensor:
    """Optional coherence regularizer.

    This nudges the oscillator field away from both total incoherence and total collapse.
    Tune target_r and weight empirically; do not assume 0.55 is universally optimal.
    """
    r = diagnostics["invariant_order_r"]
    return weight * (r - target_r).pow(2)

