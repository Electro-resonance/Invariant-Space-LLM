"""Minimal transformer integration sketch for Dynamic Invariant Space.

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

from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn

from invariant_space_layer import InvariantSpaceLayer, InvariantSpaceState


class TinyTransformerWithInvariantSpace(nn.Module):
    """A tiny transformer stack with a Dynamic Invariant Space layer inserted at the midpoint.

    This is intentionally minimal. Replace ``nn.TransformerEncoderLayer`` with your
    own GPT-style causal blocks for serious language modelling.
    """

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 256,
        nhead: int = 4,
        num_layers: int = 6,
        phase_dim: int = 12,
        max_len: int = 512,
    ) -> None:
        super().__init__()
        if num_layers < 2:
            raise ValueError("num_layers should be at least 2")
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos = nn.Parameter(torch.zeros(1, max_len, d_model))
        self.blocks = nn.ModuleList(
            [nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True) for _ in range(num_layers)]
        )
        self.invariant_index = num_layers // 2
        self.invariant_space = InvariantSpaceLayer(d_model=d_model, phase_dim=phase_dim)
        self.norm = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(
        self,
        input_ids: torch.Tensor,
        invariant_state: Optional[InvariantSpaceState] = None,
    ) -> Tuple[torch.Tensor, InvariantSpaceState, Dict[str, torch.Tensor]]:
        _b, s = input_ids.shape
        x = self.embed(input_ids) + self.pos[:, :s, :]
        diagnostics: Dict[str, torch.Tensor] = {}
        new_state = invariant_state

        for i, block in enumerate(self.blocks):
            if i == self.invariant_index:
                x, new_state, diagnostics = self.invariant_space(x, new_state)
            x = block(x)

        logits = self.lm_head(self.norm(x))
        assert new_state is not None
        return logits, new_state, diagnostics

