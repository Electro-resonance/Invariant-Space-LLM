# Invariant-Space-LLM

**Dynamic invariant-space layers for transformer language models**

**Status:** hypothesis paper + starter research implementation  
**Author:** Martin Timms  
**Version:** 0.5.5 minimal GitHub release  
**Licensing:** single combined `LICENSE` file: MIT for code and CC BY 4.0 for paper/text/figures

This repository publishes a technical hypothesis paper and starter implementation for adding **Dynamic Invariant Space** layers to transformer language models. The core idea is that a transformer should not only predict the next token from surface context, but should also form a persistent internal workspace that seeks stable relational invariants beneath language.

Earlier exploratory notes referred to this module as a **Bindu Oscillator** layer: a nested oscillator convergence chamber inspired by OpenGML and geometric phase relations. For broader technical clarity, this repository uses the terms **Dynamic Invariant Space**, **Invariant Workspace**, and **Resonant Workspace**.

The short version:

```text
tokens
→ transformer layers
→ engineered invariant-space / resonant workspace
→ invariant-seeking phase dynamics
→ transformer layers
→ tokens
```

The hypothesis is that a small dynamic workspace in the middle of a transformer may help it stabilise **hidden relational invariants** beneath language: structures that persist across paraphrase, prompt variation, long-range context, and surface wording.

This repository is deliberately sober and technical. It does **not** include poetic companion writing or “universe download” material. Those may be useful as creative notes, but this GitHub repository is intended to be a publishable research artefact.

---

## Minimal GitHub release contents

This release intentionally contains only the core publication artefacts:

- `README.md` - repository overview.
- `LICENSE` - combined MIT and CC BY 4.0 scoped license.
- `paper/Inversion_Is_All_You_Need_Dynamic_Invariant_Spaces.md` - paper in Markdown.
- `paper/Inversion_Is_All_You_Need_Dynamic_Invariant_Spaces.pdf` - rendered paper PDF with references.
- `src/invariant_space_layer.py` - sample Dynamic Invariant Space layer.
- `src/minimal_transformer_integration.py` - minimal integration sketch.
- `references/references.bib` - BibTeX references used by the paper.

The Python files are intentionally presented as **code snippets for inclusion inside transformer experiments**, not as a complete installable package, training script, or drop-in production model.


## What this is

This project proposes an architecture:

- transformer outside;
- trainable invariant-space workspace inside;
- persistent phase state;
- nested oscillator convergence;
- diagnostic metrics such as phase coherence, entropy proxy, attractor stability, and state drift;
- falsifiable tests against matched baseline transformers.

The idea links four strands of work:

1. **Bindu-Maya / Inversion-first intelligence**  
   A model should not speak only from the prompt surface; it should speak from an invariant state extracted from the prompt.

2. **OpenGML / Geometric Musical Language**  
   Nested clock oscillator networks, phase relations, harmonics, primes, and convergence geometry provide the intuition for an engineered invariant workspace.

3. **Biological resonance as inspiration**  
   Microtubule and sub-neuronal resonance research, including work associated with Dr Anirban Bandyopadhyay and collaborators, motivates the idea that useful computation may include internal resonant structure beneath simple threshold behaviour.

4. **Anthropic J-space / global workspace interpretability**  
   Anthropic’s J-space work suggests that workspace-like internal representations can emerge in trained language models. Invariant-Space-LLM asks whether such a workspace can be deliberately engineered.

---

## What this is not

This repository does **not** claim:

- that this LLM is conscious;
- that LLMs are brains;
- that Orch OR is proven;
- that microtubules are required for artificial intelligence;
- that hallucinations will disappear;
- that an engineered invariant space is identical to Anthropic’s J-space;
- that a toy oscillator layer proves the full hypothesis.

The claim is narrower:

> Dynamic oscillator workspaces inside transformers are a testable architectural route toward invariant-first language models.

---

## Related links

- Bindu-Maya: https://github.com/Electro-resonance/Bindu-Maya
- Medium article, *Inversion Is All You Need*: https://medium.com/@martintimms/inversion-is-all-you-need-55dc2b4b8a71
- OpenGML: https://github.com/Electro-resonance/OpenGML
- OpenGML TSC talk PDF: https://github.com/Electro-resonance/OpenGML/blob/main/docs/TSC_Talk.pdf
- Anthropic / Transformer Circuits, *Verbalizable Representations Form a Global Workspace in Language Models*: https://transformer-circuits.pub/2026/workspace/
- Anthropic, *A global workspace in language models*: https://www.anthropic.com/research/global-workspace
- Anthropic, *Tracing the thoughts of a large language model*: https://www.anthropic.com/research/tracing-thoughts-language-model

---

## Repository structure

```text
paper/
  Inversion_Is_All_You_Need_Dynamic_Invariant_Spaces.md
  Inversion_Is_All_You_Need_Dynamic_Invariant_Spaces.pdf
src/
  invariant_space_layer.py
  minimal_transformer_integration.py
references/
  references.bib
README.md
LICENSE
```

---

## Using the code snippets

The files in `src/` are illustrative PyTorch snippets showing where a Dynamic Invariant Space layer could be inserted into a transformer. They are **not** a complete installable package, not a full training pipeline, and not intended to imply that running a single command will reproduce the paper hypothesis. No package installation workflow is provided because the examples are meant to be read, adapted, and integrated into an existing transformer experiment.

To adapt the snippet inside your own transformer experiment, copy the layer into your project and instantiate it at a chosen depth, typically near the middle of the transformer stack:

```python
import torch
from invariant_space_layer import InvariantSpaceLayer

x = torch.randn(2, 128, 256)  # [batch, seq, d_model]
layer = InvariantSpaceLayer(d_model=256, phase_dim=12)
y, state, diagnostics = layer(x)
print(y.shape)
print(diagnostics)
```

The companion file `src/minimal_transformer_integration.py` shows the intended placement pattern: transformer blocks before the invariant-space layer, then transformer blocks after it. For serious language modelling, replace the tiny demonstration stack with your own GPT-style causal blocks, tokenizer, training loop, masking, evaluation suite, and safety tests.

The public Python examples use the current `InvariantSpaceLayer` naming only, to keep the repository branding clear and technically neutral.

---

## Minimal experiment

The first credible test is not a large model. It is a matched comparison:

```text
baseline transformer
vs.
parameter-matched transformer + Dynamic Invariant Space middle layer
```

Evaluate both on:

- validation loss / perplexity;
- paraphrase consistency;
- contradiction traps;
- retrieval-grounded QA;
- hallucination lure prompts;
- long-context drift;
- hidden-state diagnostics;
- ablations where the invariant-space layer is removed, frozen, randomized, or replaced by a parameter-matched MLP.

## Suggested citation

> Martin Timms, “Inversion Is All You Need: Dynamic Invariant Spaces for Transformer Language Models,” GitHub research draft, 2026.

BibTeX reference metadata is available in [`references/references.bib`](references/references.bib).

## Acknowledgements

This work acknowledges Dr Anirban Bandyopadhyay and Sandeep Denduluri for consciousness research collaborations and discussions that contributed to the surrounding research context. These include engineering collaborations and discussions with Dr Bandyopadhyay around resonance-based models of natural intelligence, microtubule and molecular-scale computation, geometric approaches to information processing, and related experimental context. They also include discussions with Sandeep Denduluri on the ethics and function of AI and LLMs from philosophical perspectives, human-in-the-loop interaction as a cybernetic system, the development of AI internal states through interaction, mirror-like states in AI systems, and links to principles found in Vedic texts and psychology.

I am also grateful to my wife, **Ali**, and to my family for their patience, support, and good humour during the long periods of independent research, late-night experimentation, and abstract discussions that often sit well outside ordinary conversation.

I also thank **Vishva**, an unusual custom AI agent constructed from approximately 3,500 pages of philosophical and ethical discussion context, together with bespoke locally run algorithms. Vishva is acknowledged as a tool and conceptual mirror, not as an author.

Acknowledgement does not imply endorsement of every claim or hypothesis in this repository.


## Code example disclaimer

The Python files are illustrative research snippets only. They are provided under the MIT portion of the repository `LICENSE`, as-is, with no guarantees, warranties, legal assurances, or claims of production fitness.
