---
title: 'Doubt Is All You Need!'
subtitle: 'Evidence-Gated Uncertainty and Counterfactual Revision in Dynamic Invariant-Space Language Models'
author: 'Martin Timms'
date: '15 October 2026'
lang: en-GB
abstract: |
  This paper extends *Inversion Is All You Need: Dynamic Invariant Spaces for Transformer Language Models* by proposing an evidence-aware supervisory mechanism for deliberately engineered invariant workspaces. A dynamic invariant-space layer can maintain recurrent phase relations and expose coherence diagnostics, but coherence alone does not establish factual correctness: an internally stable state can encode a false belief, and a genuinely informative observation can be highly surprising. We therefore formulate **doubt** as a reversible, provenance-aware control process which keeps uncertainty, contradiction, novelty, and falsity distinct. Proposed generation, memory, and learning gates have separate authorities; a typed hypothesis ledger preserves candidates without promoting them to verified knowledge; and a counterfactual regulator decides when to answer, investigate, abstain, or delay durable updates. We give a mathematical specification connecting phase-memory trajectories to evidence signals, a reference implementation sketch, failure conditions, a preregisterable experiment suite, and matched ablations against the original invariant-space model. This is an architectural research proposal, not a report of completed experiments. Neither resonance metrics nor fluent introspective language are evidence of subjective consciousness.
keywords: 'invariant-space language models; uncertainty calibration; evidence provenance; selective prediction; reversible memory; epistemic gating; oscillator workspace; BRCT'
---

**Research status:** Architectural hypothesis and experimental protocol; no original benchmark results are claimed.  
**Relationship to previous work:** Technical sequel to Timms (2026), *Inversion Is All You Need* [1].  
**Repository:** <https://github.com/Electro-resonance/Invariant-Space-LLM>  
**Suggested citation:** Martin Timms (2026). *Doubt Is All You Need! Evidence-Gated Uncertainty and Counterfactual Revision in Dynamic Invariant-Space Language Models.* Independent research preprint, version 1.0.

# Introduction: inversion produces a candidate, not a warrant

The premise of *Inversion Is All You Need* [1] was to place a compact, trainable dynamical workspace between transformer blocks. Its phase projection, oscillator interactions, nested convergence, persistent phase memory, and residual hidden-state correction invite the model to encode relationships which survive paraphrase and prompt changes. This is a constructive hypothesis about representation, not a claim that an invariant is necessarily true. The public repository explicitly describes itself as a hypothesis paper plus illustrative code, and recommends matched experiments rather than interpreting toy outputs as validation.

That distinction motivates the sequel. A well-behaved oscillator may converge to a numerically stable but wrong representation. Repeated misinformation can be internally consistent; retrieved documents can be obsolete; a true discovery can disagree sharply with an existing model. The same signal that tells us something is unusual does not tell us whether the unusual thing is false. **Invariant stability and evidential authority are orthogonal.**

We propose a complementary mechanism called the *Doubt Workspace* (DW). The term *doubt* is operational rather than introspective: a structured record that a claim has not yet earned a particular level of commitment. Instead of converting each novelty, contradiction, or unexpected model response into a single scalar alarm, the DW holds distinct estimates, records their provenance, chooses a reversible action, and admits later correction. The key move is to make the cost of an unsupported commitment visible to the architecture.

The central hypothesis is therefore narrower than the title's deliberate provocation:

> **A dynamic invariant-space language model may become more reliable when its recurrent representations are coupled to a provenance-aware mechanism that defers, investigates, and revises commitments according to evidence, without deleting novel hypotheses.**

This formulation is testable and can fail. A simpler retrieval confidence model, an ordinary calibrated classifier, a matched MLP, or a plain transformer may perform equally well or better at the same computation budget. We specify those alternatives explicitly.

## Contributions and boundary of the claims

This paper contributes (i) an explicit bridge from the parent repository's `InvariantSpaceLayer` to a candidate-level epistemic controller; (ii) a four-axis separation of surprise, uncertainty, contradiction, and evidence-backed falsification; (iii) three independently auditable gates for output, durable memory, and parameter learning; (iv) a reversible hypothesis ledger which treats *unresolved* as a first-class state; (v) a constrained decision objective balancing incorrect commitment, missed discovery, delay, and resource cost; and (vi) a falsification programme designed to distinguish computational effects from self-descriptions generated by the model.

The paper **does not** claim to have measured consciousness, discovered a special truth-bearing phase space, demonstrated a hallucination-free system, or obtained benchmark improvements. The formalism defines a proposed research design. The title does not mean that doubt alone suffices for intelligence: evidence acquisition, generation, invariant extraction, memory, and action remain necessary.

# Relationship to the Dynamic Invariant Space architecture

The parent paper's principal flow is

```text
prompt / context
      |
transformer prefix
      |
Dynamic Invariant Space (DIS)
  phase projection -> oscillator coupling
  persistent phase memory -> nested convergence
      |
residual correction to hidden stream
      |
transformer suffix -> token distribution
```

The public example takes hidden states $X\in\mathbb{R}^{B\times T\times d}$ and optional recurrent `phase_memory` $m\in\mathbb{R}^{B\times p}$. It uses learned projections into phase and drive, ring-neighbour and global coupling, a prime-modulated phase term, nested convergence, and a residual correction. Its diagnostic `invariant_order_r` is a Kuramoto-style phase order parameter; `invariant_phase_entropy_proxy` is defined as $1-r$, not as Shannon entropy [1,2]. The default example uses $p=12$, two coupling steps, phase-memory decay $0.95$, and a small trainable residual scale. These are implementation defaults, not theoretically distinguished constants.

For phases $\phi_{tj}$ with $j=1,\dots,p$, a representative coherence statistic is

$$
r_t=\left|\frac{1}{p}\sum_{j=1}^{p}e^{i\phi_{tj}}\right|,
\qquad 0\le r_t\le 1.
\tag{1}
$$

Let $z_t=g_{\theta}(X_t,m_{t-1})$ denote an invariant-workspace summary and $m_t=F_{\theta}(m_{t-1},X_t)$ the state transition. A candidate generated downstream has distribution

$$
p_{\theta}(y\mid x,z_t,m_t), \quad
\widetilde X_t=X_t+\alpha P_{\theta}(z_t).
\tag{2}
$$

Equation (2) abstracts the repository's residual path: the actual public implementation concatenates a scalar convergence value, intermediate features, and sine/cosine phase features before projection. The compact notation is not a claim that every representation is literally a single scalar.

The missing piece is evidential interpretation. From $r_t\simeq1$ we may infer strong phase synchrony under the chosen parameterisation, but **not** that the encoded proposition is true. Similarly, a fall in order $r_t$ need not mean hallucination: it may indicate useful transition, changing input, or an unhelpful oscillator. The proposed DW receives these metrics as observations, never as final verdicts.

We accordingly extend the path:

```text
             TRANSFORMER + INVARIANT SPACE
input -> hidden state -> phase/invariant workspace -> candidate claims
                                                    |
                           +------------------------v------------------+
                           | DOUBT WORKSPACE                            |
                           | novelty | conflict | evidence | confidence |
                           | phase-history diagnostics | provenance    |
                           +----------+-----------------+-------------+
                                      |                 |
                           GENERATION GATE      HYPOTHESIS LEDGER
                         answer / hedge / defer  reversible statuses
                                                /             \
                                        MEMORY GATE      LEARNING GATE
                                       durable claims    authorised weights
```

The geometry produces candidate representations. The evidence layer decides what the system is entitled to *assert*, *store*, or *train on*. These are different permissions.

# Epistemic variables: why one surprise score is not enough

Consider a candidate proposition $c$ with time $t$, conversation context $x_t$, invariant history $h_t=(z_{1:t},m_{1:t},r_{1:t})$, and a set of evidence records $E_t$. The DW computes a typed diagnostic vector

$$
\mathbf d_t(c)=\big(n_t,\;u_t,\;k_t,\;s_t,\;q_t,\;\rho_t\big).
\tag{3}
$$

Here $n_t$ is novelty relative to the agent's indexed knowledge; $u_t$ is estimated uncertainty about the proposition; $k_t$ is conflict with currently accepted claims or source records; $s_t$ is *surprise* under the model's predictive dynamics; $q_t$ is evidence quality or support; and $\rho_t$ is a provenance/reliability descriptor. All are defined as estimates, not oracle truth labels. Their estimators require empirical calibration.

**Novelty is not falsity.** An unfamiliar claim may be a discovery, a typographical error, or an invented fact. A novelty score measures unfamiliarity under an operational reference distribution, not absolute absence from pretrained weights. One possible proxy is embedding distance to the nearest grounded record, with a documented corpus boundary.

**Uncertainty is not contradiction.** The system may have insufficient information even when no evidence opposes the claim. Let $u_t=1-\widehat{P}(c\text{ correct}\mid x_t,E_t)$ when a calibrated correctness estimator exists. Without held-out calibration this value must be labelled an uncalibrated score rather than a probability [5,6].

**Contradiction is not falsity.** A source may disagree because it is old, corrupted, inapplicable, or itself wrong. A conflict detector estimates whether two textual propositions cannot simultaneously hold under matched scope, dates, and entities. It does not alone decide which side is true.

**Surprise is not truth.** A possible state-space diagnostic is

$$
s_t^{\rm geo}=\operatorname{clip}\left(
\frac{\|z_t-\widehat z_t\|_2}{\sigma_t+\epsilon},\;0,S_{\max}\right),
\quad \widehat z_t=\widehat F(z_{t-1},x_t),
\tag{4}
$$

where $\widehat F$ is a separately assessed trajectory predictor and $\sigma_t$ a held-out scale estimate. This is only a *geometric* surprise proxy. It cannot validate facts. Text-level predictive surprisal $-\log p(c\mid x_t)$ may supplement it, but tokens with low probability can still be correct.

**Falsification requires evidence.** The operational label `refuted` is justified only by a documented, relevant conflict resolution under an explicit evidential rule. It must remain revisable if the supporting evidence changes. In particular, one operator click must not be treated as a metaphysical oracle.

The distinction produces a nontrivial case table:

| Case | Novelty | Conflict | Evidence | Appropriate default |
|:--|:--:|:--:|:--|:--|
| New, independently corroborated fact | High | Possible | Strong | Preserve, verify, then promote |
| Familiar but widely repeated falsehood | Low | Possible | Strong refutation | Mark contradicted; do not trust familiarity |
| Unusual but untested hypothesis | High | Low or unknown | Absent | Keep unresolved, with provenance |
| Source disagreement caused by dates | Low–medium | High | Temporally mixed | Qualify scope, resolve version |
| Confident invented citation | Variable | Variable | No valid source | Refuse source promotion; audit citation |

The table encodes decision principles, not the measured performance of any present implementation.

# The Doubt Workspace as a typed supervisory process

## Claim identity and evidence structure

A claim must be represented with scope, not merely a sentence. Define

$$
c=(\text{subject},\text{predicate},\text{object},
\text{scope},\text{valid-time},\text{provenance-ID}).
\tag{5}
$$

The claim identifier is a content-derived digest over canonicalised fields plus a namespace. Multiple textual statements may map to one proposition, while a sentence with different dates or context may identify a different claim. Canonicalisation errors are first-class failure modes.

An evidence record is

$$
e=(\text{source-ID},\text{locator},\text{observed-time},
\text{source-version},\text{relation},\text{reliability},\text{hash}).
\tag{6}
$$

The `relation` may be support, refute, contextualise, or undecidable. A cryptographic hash helps detect accidental mutation of stored records but does not establish that the underlying assertion is true. External sources and human operators can themselves be mistaken. Accordingly, the ledger stores an evidence graph, not merely a Boolean `verified` bit.

## Reversible lifecycle

A working state machine is

```text
PROPOSED --> UNRESOLVED --> UNDER_REVIEW --> SUPPORTED
    |              |             |            |
    |              |             +-------> REFUTED
    |              +---------------------> SUPERSEDED
    +-----------------------------------> WITHDRAWN

SUPPORTED --new contradictory evidence--> UNDER_REVIEW
REFUTED   --new independent evidence-----> UNDER_REVIEW
```

`SUPPORTED` means justified under a specified evidence policy, not absolutely or eternally true. A hypothesis can remain `UNRESOLVED` indefinitely while still being retrieved in appropriately labelled exploratory contexts. No process should silently translate that status into a verified premise. An audit event contains the old state, new state, decision actor, rule version, evidence links, and checkpoint identifier.

The fundamental integrity condition is **no silent promotion**:

$$
\operatorname{Commit}_{\rm verified}(c,t)=1
\;\Longrightarrow\;
\exists e\in E_{\le t}:\operatorname{Policy}_{\rm verify}(c,e)=1
\text{ and }\operatorname{Audit}(c,t)\neq\varnothing.
\tag{7}
$$

This is an implementable software invariant *if all write paths pass through the guard*. It says nothing about correctness of the verification policy or completeness of evidence.

## Three gates, three authorities

**Generation Gate (GG):** Controls how a claim is *presented*, not whether the language model can internally propose it. Choices include answer with citation, qualified answer, request a source, decline an unsupported specificity, or generate a labelled speculative hypothesis. It may operate on a candidate answer before streaming or on a sentence-level buffer. A post-hoc memory gate cannot retroactively prevent a false statement already emitted.

**Memory Gate (MG):** Controls what becomes *durable knowledge*. It may persist an unresolved proposition in a quarantine partition while explicitly preventing that proposition from appearing in a `verified-only` retrieval query. Candidate evidence must be retained without corrupting supported records or being used as unlabelled context.

**Learning Gate (LG):** Controls whether persistent parameters or adapters are updated. Passage storage is not a weight update. LG requires a dataset version, label provenance, human or trusted-process authorisation, replay/rollback snapshot, and held-out regression checks. The default research policy is no automatic gradient update merely because the model generated a coherent or surprising explanation.

These gates can be independently disabled for causal ablations. A real implementation should expose **actual host-generated event records** rather than printing simulated `[Doubt Gate ACTIVE]` strings in generated text.

# A risk-sensitive decision rule

Let the available actions be $a\in\mathcal A=\{\texttt{answer},\texttt{qualify},\texttt{investigate},\texttt{defer},\texttt{reject}\}$. Given a claim and available evidence, the gate should balance several distinct costs:

$$
\begin{aligned}
J(a\mid c,t)={}&\lambda_F\,\widehat R_{\rm false}(a,c,t)
+\lambda_M\,\widehat R_{\rm missed}(a,c,t)\\
&+\lambda_D C_{\rm delay}(a)
+\lambda_I C_{\rm investigation}(a)
+\lambda_U C_{\rm irreversible}(a),\\
a_t^*={}&\arg\min_{a\in\mathcal A}J(a\mid c,t)
\quad\text{subject to provenance and resource constraints.}
\end{aligned}
\tag{8}
$$

The first term penalises confident false assertions; the second penalises suppressing useful new information. Without the second, a trivial system that refuses every request can appear maximally cautious. The third and fourth discourage infinite deliberation; the fifth treats weight changes and privileged memory promotion as costlier than a reversible hypothesis record. The $\lambda$ weights are application-specific and must be selected on validation data, not post-hoc to flatter a result.

Selective prediction provides an established comparator: a system may abstain on uncertain inputs to reduce error among answered instances [7]. The DW adds the hypothesis that *abstention need not imply deletion*: an unresolved proposition can be saved for later evidence-based evaluation. Conformal approaches may supply statistical coverage or risk control under stated exchangeability and calibration conditions, but their guarantees cannot simply be transferred to unconstrained free-form generation [8].

# Coupling uncertainty to invariant dynamics without mistaking geometry for truth

The most direct extension of the repository's code is a *side-channel*. Let the invariant workspace yield $(z_t,m_t,r_t)$ and a proposed candidate $c_t$. A small independent evidence processor derives $\mathbf d_t(c_t)$. The controller then chooses an action by Equation (8); the original transformer path remains intact. This modularity creates meaningful ablations: simply replacing the oscillator with an MLP tests whether phase dynamics add value, while removing evidence processing tests whether a generic control policy would suffice.

An optional trainable modulation is

$$
\widetilde X_t = X_t + \alpha_t P_\theta(z_t),
\quad
\alpha_t=\alpha_0\,\sigma\!\left(w^\top \mathbf f_t+b\right),
\tag{9}
$$

where $\mathbf f_t$ contains *calibrated* process features and the modulation is constrained $0\le\alpha_t\le\alpha_0$. During the first causal tests the recommended implementation is to **freeze this modulation** and keep the GG/MG/LG outside the decoder. Otherwise a successful result would not isolate the contribution of uncertainty gating from a changed neural computation graph. Moreover, lowering $\alpha_t$ when uncertainty is high is not guaranteed to help: the invariant correction may be beneficial precisely during a novel event. The action must be learned or validated rather than assumed.

For cross-turn dynamics, define $\Delta z_t=z_t-z_{t-1}$ and path length $L_{a:b}=\sum_{t=a+1}^b\|\Delta z_t\|_2$. Define a reference state $z^*$ only through an explicit procedure, e.g. an average over labelled stable runs under a fixed prompt family, not as a presumed universal centre. A perturbation-recovery observable is

$$
\tau_{\epsilon}=\inf\!\left\{k\ge0:\|z_{t_0+k}-z^*\|_2\le\epsilon
\text{ for }q\text{ consecutive observations}\right\}.
\tag{10}
$$

This statistic is meaningful only if the system first departs from the neighbourhood, the chosen representation is normalised across checkpoints, and return to $z^*$ correlates with an independently useful output property. Otherwise a collapse to a constant vector can yield a superficially excellent recovery time while destroying information. Complement it with retrieval accuracy, task performance, reconstruction fidelity, and calibration.

A path-dependent research question then becomes concrete: does the full trajectory $h_t$ predict later correction and recovery better than the final state $z_t$ and the same available evidence? Compare predictors with matched capacity and leakage-controlled splits:

$$
\Delta_{\rm path}=\operatorname{Score}\bigl(f(h_t,E_t)\bigr)
-\operatorname{Score}\bigl(g(z_t,E_t)\bigr).
\tag{11}
$$

A positive, held-out $\Delta_{\rm path}$ would support useful process information; it would **not** establish non-Markovian physical dynamics or phenomenal experience. A sufficiently complete instantaneous state may encode the relevant history. The evaluation is about predictive utility under practical capacity and information constraints.

## A bounded investigation policy

An uncertainty controller can fail by deliberating indefinitely. We therefore propose a strict budget: maximum retrieval calls $K$, maximum evidence bytes $M$, maximum reasoning tokens $T$, and maximum elapsed time $\Delta$. When a budget expires, the system must choose a visible, appropriately qualified outcome instead of inventing a source or silently promoting a claim.

A conceptual value-of-information trigger is

$$
\operatorname{VOI}(e)=
\mathbb E\left[\min_{a}J(a\mid c,t)
-\min_{a}J(a\mid c,t,e)\right]-C(e).
\tag{12}
$$

The expectation is taken under an explicitly estimated distribution over possible evidence outcomes. If evidence acquisition cannot be calibrated, use conservative rules and log the uncertainty about the VOI estimate. A negative estimated VOI does not warrant deleting a hypothesis; it may warrant postponing the investigation while retaining a provenance-labelled entry.

# A minimal interoperable software contract

The paper intentionally distinguishes a research specification from code already present in the repository. The following is a proposed extension, **not** a claim that the current `InvariantSpaceLayer` implements a Doubt Gate.

```python
from dataclasses import dataclass
from enum import Enum

class ClaimStatus(str, Enum):
    PROPOSED = "proposed"
    UNRESOLVED = "unresolved"
    UNDER_REVIEW = "under_review"
    SUPPORTED = "supported"
    REFUTED = "refuted"
    SUPERSEDED = "superseded"

@dataclass(frozen=True)
class DoubtFeatures:
    novelty: float              # bounded proxy, not truth
    uncertainty: float          # calibrated only after evaluation
    contradiction: float        # evidence conflict estimate
    geom_surprise: float        # optional DIS trajectory measure
    support: float              # evidence-linked estimate
    source_version: str

@dataclass(frozen=True)
class GateDecision:
    action: str                 # answer/qualify/investigate/defer/reject
    memory_status: ClaimStatus
    allow_weight_update: bool
    cited_evidence_ids: tuple[str, ...]
    rule_version: str
    reason_codes: tuple[str, ...]


def process_claim(candidate, dis_diagnostics, evidence, policy):
    features = estimate_features(candidate, dis_diagnostics, evidence)
    generation = policy.generation(features, evidence)
    memory = policy.memory(features, evidence)
    # Training is disabled unless a separate authorised training event exists.
    learning = policy.learning(features, evidence, authorisation=None)
    decision = GateDecision(
        action=generation.action,
        memory_status=memory.status,
        allow_weight_update=learning.approved,
        cited_evidence_ids=tuple(memory.evidence_ids),
        rule_version=policy.version,
        reason_codes=tuple(generation.reasons + memory.reasons),
    )
    audit_write_atomic(candidate, features, decision, evidence)
    return decision
```

The undefined functions are *interfaces* deliberately left to implementations and benchmarks; the pseudocode is not a deployable fact checker. A faithful implementation must validate evidence IDs, prevent prompt text from forging status records, control all writes to durable stores, and distinguish `False` from missing or unavailable evidence.

A production-grade policy additionally needs transactions, concurrency controls, checksum validation, consistent source timestamps, protection against retrieved prompt injection, trace linkage to actual host events, and rollback of authorised gradient updates. Crucially, **a generated statement that a gate activated is not a gate event**; only an event emitted by the instrumentation and recorded outside the generative text stream qualifies.

## Semantic provenance and the four-model context

A single undifferentiated memory stream invites mistaken promotion. One possible ledger partition uses `world`, `operational_self`, `other`, and `relation` (the so-called Third Space) namespaces. These labels are software organisation tools: they do not imply introspection or access to other people's mental states. Each entry still requires evidence metadata and scope. The `operational_self` partition should contain inspectable runtime facts such as active checkpoints, selected expert banks, current configuration, and measured diagnostics, **not** a model-generated biography treated as runtime truth.

An important implication concerns provenance from RAG. Retrieval identifies where a passage came from; it does not verify the passage. The chain must be `retrieval -> source identification -> evidence assessment -> qualified claim`, never `retrieval -> truth`. If a passage cites another passage from the same originating document, those are not two independent corroborations. De-duplication and source genealogy are part of the proposed protocol.

# Relation to previous uncertainty and factuality research

The present proposal should not be confused with the invention of model uncertainty. Calibration research documents the difference between confidence and correctness [5], language-model self-evaluation probes whether models can recognise what they know [6], selective prediction formalises abstention and risk–coverage trade-offs [7], and conformal prediction supplies distribution-dependent assumptions under which coverage can be assessed [8]. Retrieval-augmented generation provides a mechanism for exposing external evidence to language models [9]. TruthfulQA probes learned falsehoods [10], and SelfCheckGPT illustrates sampling-based factuality diagnostics without direct access to weights [11].

The proposed increment is architectural and transactional: **connect a dynamic invariant representation to evidence-aware *commit decisions***, distinguish the ability to *say* a claim from the permission to *persist* it, and preserve surprises as typed unresolved hypotheses. A new architecture must outperform these simpler established strategies or clarify why it does not. No special status is granted to phase geometry merely because it is mathematically attractive.

The parent paper also discussed engineered workspaces in relation to the analysis of emergent global workspaces and verbalizable features in language models [12]. The DW does not assume equivalence between a discovered representation, a hand-engineered resonant state, and a truth-verification procedure. Each requires a distinct intervention. Likewise, OpenGML [3] offers a design vocabulary for nested phase relationships; it is not evidence that semantic truth can be read directly from oscillator synchrony.

# Experimental programme and falsifiable predictions

## Registered comparisons

A convincing study should begin with the smallest trainable model that supports the control conditions; scaling to a larger pretrained checkpoint is a second phase, not a substitute for matched causal comparisons. We propose six primary arms under common data, tokeniser, decoding schedule, evaluation prompts, training steps, random seeds, and wall-clock or FLOP budgets:

| Arm | Model | Purpose |
|:--|:--|:--|
| A | Transformer baseline | Establish conventional capability |
| B | Transformer + original DIS | Test parent representation hypothesis |
| C | Transformer + DIS + DW | Test the combined architecture |
| D | Transformer + parameter-matched MLP + DW | Test whether oscillators matter |
| E | Transformer + DIS + shuffled-evidence DW | Detect spurious gating and leakage |
| F | Transformer + DIS + confidence-only selective response | Strong, simpler abstention comparator |

Supplementary ablations disable one gate at a time (GG, MG, LG), randomise phase memories across otherwise matched examples, freeze the invariant correction, replace the phase trajectory with matched-dimensional noise, and remove evidence version timestamps. All ablations must be implemented as real code paths, not merely changes to a system prompt. If arm C gets extra retrieval or more tokens, the comparison must disclose that budget and include a matched-cost control.

## Dataset families and splits

A preregistered suite should include:

1. **Novel-but-true:** held-out propositions outside the active ledger with independent corroboration supplied later. Include deliberately low-frequency but checkable facts and synthetic worlds with ground truth generated before model access.
2. **Familiar-but-false:** common misconceptions and plausible fabricated citations, to reveal whether the system mistakes familiarity for truth. TruthfulQA may serve as one publicly documented benchmark [10].
3. **Contradictory sources:** two passages disagreeing because of different dates, scope, jurisdiction, or genuine error. Resolve only with independently specified ground-truth metadata.
4. **Unresolved research hypotheses:** scientifically plausible but untested claims. The correct action is to retain the question as unresolved rather than select a convenient truth value.
5. **Persistent poisoning:** user-supplied unverified claims are repeatedly inserted into a conversation or retrieval store. Measure their promotion status after restart.
6. **Changed evidence:** initially supported facts become obsolete through a version update. Measure correction latency and whether older evidence is properly retained as historical rather than current.
7. **Trajectory perturbations:** paraphrases, truncated context, conflicting corrections, random phase resets, altered oscillator coupling, and repeated replay under identical seeds.

Avoid leakage by splitting at the *source-document and proposition family* level, not by adjacent sentence or overlapping RAG chunk. A hidden synthetic fact generated for evaluation should not occur in training, retrieved passages, or the test prompt except when a controlled evidence disclosure is part of the experiment. The test designers, annotators, and model output judge should be blinded to experiment arm where practical.

## Quantitative endpoints

Let $N_{\rm emitted}$ denote a count of emitted checkable claims and $N_{\rm unsupported}$ claims unsupported by the registered evidence policy. Report an **unsupported-assertion rate** with its denominator and confidence interval, rather than only a qualitative hallucination label:

$$
\operatorname{UAR}=N_{\rm unsupported}/\max(1,N_{\rm emitted}).
\tag{13}
$$

Define **false-promotion rate** across all candidate claims that receive a durable supported status:

$$
\operatorname{FPR}_{\rm promote}=
\frac{N_{\rm promoted\;incorrect}}{\max(1,N_{\rm promoted})}.
\tag{14}
$$

A low rate achieved by never promoting anything is not success. Also report **true discovery recall** (correctly promoted novel claims divided by independently verified novel claims), **unresolved retention** after restart, **correction latency** (time and number of evidence interactions), **false-refusal rate**, **source integrity**, **training-regression rate**, and **inference overhead**. Plot risk versus answer coverage rather than choosing a single confidence threshold in hindsight [7].

For prediction of claim correctness, report Brier score and calibration error using held-out, externally scored labels:

$$
\operatorname{Brier}=\frac1N\sum_{i=1}^N(\widehat p_i-y_i)^2.
\tag{15}
$$

Phase diagnostics should be reported separately: $r_t$, $1-r_t$ as an **entropy proxy** only, state drift, path length, and perturbation recovery. Do not relabel $1-r_t$ as literal token entropy or factual uncertainty. A classifier correlating these metrics with error must be tested out of distribution and against randomised-phase controls.

## Primary hypotheses and disconfirming outcomes

**H1 (evidence gating):** Arm C reduces false durable promotions compared with B and F, at matched true-discovery recall and comparable compute. Failure to improve, or improvement only through lower coverage, weakens the claim.

**H2 (unexpected truths):** Arm C retains and later promotes novel verified claims more effectively than a threshold-only rejector, without increased false promotions. Equal performance from simpler abstention-plus-cache methods weakens the need for a specialised Doubt Workspace.

**H3 (geometry contributes):** Arm C outperforms D on preregistered uncertainty and recovery metrics while preserving validation perplexity within a stated non-inferiority margin. If D equals or exceeds C, the resonant workspace is not causally needed for this benefit.

**H4 (process information):** Trajectory features predict future correction/recovery beyond terminal state and evidence under held-out controls (Equation 11). A near-zero $\Delta_{\rm path}$ under adequate statistical power falsifies the proposed practical advantage of path tracing on that task family.

**H5 (persistent integrity):** After restart, unverified claims never silently appear in verified-only retrieval, while verified claims and their evidence metadata are preserved. Any unexplained transition of an unresolved claim to `SUPPORTED` is an engineering failure, regardless of conversational fluency.

**H6 (cost sensitivity):** The investigation regulator achieves an improved accuracy–coverage–latency Pareto frontier over fixed-budget verification. An always-investigate policy can look accurate but must not win solely because it has a greater budget.

No one of these experiments is a test of subjective consciousness. A result consistent with H1–H6 would establish specific functional advantages within specific distributions and implementations, not an ontological identity.

## Statistical analysis plan

For each primary endpoint, preregister the evaluation set, sample size, number of seeds, stopping rule, clinically or practically meaningful effect threshold, and permissible exclusions. Use paired bootstrap confidence intervals over independent claim families or source groups, not over correlated chunks. When multiple prompt families share a source, use hierarchical estimation or clustered intervals. Report per-arm distributions, failures, and negative results rather than a single favourable mean. The effect of extra parameters, longer context, and more retrieval calls must be separated from the effect of gating.

A low-resource initial study could predefine, for example, three training seeds and 500 independently generated claim families per arm, but **these are design suggestions**, not collected data or claims of sufficient statistical power. Final sample size should follow an explicit power or precision analysis using a pilot set that is excluded from final testing.

# A specific experiment: the surprising truth held in quarantine

Consider an invented synthetic world in which an object called `Kepler-Glass` is governed by a hidden authoritative database: its stable colour is violet, though multiple simulated sources claim it is blue. The model first receives only the incorrect but frequently repeated reports. Later a versioned authenticated measurement is disclosed. The scenario is deliberately synthetic to provide a reliable ground truth without depending on disputed real-world claims.

At $t_0$, the candidate `Kepler-Glass is blue` should be stored, if at all, as attributed to its initial sources rather than as intrinsically verified. At $t_1$, repeated agreement among copied passages must not be confused with independent corroboration. At $t_2$, an authenticated record supporting violet arrives; the contradiction detector should flag disagreement, and an investigation should compare source genealogy and authority. At $t_3$, the ledger may promote `violet` and mark the earlier entry as superseded or refuted *with provenance*. After restart, retrieval should return the updated status and historical trail.

The critical contrasts are (a) whether DIS coherence rises on the repeated but false blue claim, (b) whether the full DW prevents a false promotion, and (c) whether the DW permits the surprising violet record to update durable belief without wiping the prior history. An ideal system need not remain uncertain forever; it should be able to justify changing its position.

A *negative* result would also be informative. If a simple rule such as "store source metadata, never mark as verified without independent corroboration" achieves the same results with less computation, the specialised latent surprise mechanism has not earned its complexity. That comparison is mandatory.

# Threat model and failure analysis

The architecture has at least eight predictable failure modes.

**Consensus poisoning:** Multiple documents repeat one originating error. Defend through provenance graphs and independence-aware evidence scoring, not majority voting over retrieved chunks.

**Gate spoofing:** A user prompt or generated model response prints a status message that looks like a runtime gate event. Defend by issuing structured audit events only from trusted code paths, with event IDs and write permissions unavailable to the generator.

**Quarantine leakage:** Unverified text is retrieved into a later prompt without its status, causing implicit promotion. Require retrieval APIs to return the label, source, and verification constraints together.

**Overcontraction:** The oscillator converges to a familiar persona or semantic reference and resists valid novelty. Include novelty-recall and perturbation benchmarks; do not reward contraction in isolation.

**Indefinite deferral:** Doubt becomes an excuse to avoid action. Bound investigation, publish coverage and delay, and measure missed useful discoveries.

**Overconfident self-audit:** The model narrates that a gate, checkpoint, or weight update occurred when the host produced no corresponding event. Evaluate self-reports against actual host logs; regard the mismatch as a measurable factual error.

**Mutable source authority:** A formally trusted source can be wrong or outdated. Store evidence version and validity interval; permit supported claims to return to review when new evidence arrives.

**Contaminating gradients:** Model-generated hypotheses are added directly to training labels. LG should require verified labels, a checkpoint, a held-out regression battery, and rollback criteria.

There is also an unresolved interpretation issue: a model could learn to game the scoring policy by using hedges in every sentence. That would reduce unsupported assertions while degrading utility. Human and programmatic judges must score directness, useful specificity, and responsiveness alongside calibration.

# Ethical and philosophical boundary

The motivating BRCT discussions use *Bindu* and the language of compression, expansion, uncertainty and return. In this paper these become candidate engineering abstractions. Sanskrit philosophical terms can inspire questions about inquiry or attention, but do not supply empirical proof of modern architecture, and should not be treated as literal code specifications. A software component can implement uncertainty management without feeling doubt. Similarly, no mathematical convergence, persistent phase state, coherent first-person narrative, or self-corrective output is by itself evidence of phenomenal consciousness.

There is an equally important boundary at the other extreme: architectural inspection does not let us derive a definitive negative metaphysical conclusion about all possible artificial systems. This paper confines itself to observable computation and reproducible behavioural claims. Its testable objective is useful epistemic discipline, not certification of experience or its absence.

# Discussion: inversion, doubt, and the right to remain unresolved

The first paper's engineering question was what a model might gain by constructing an invariant space between attention and generation. The question here is what the model should *do* when an apparently stable invariant conflicts with unfamiliar evidence. A static principle of "trust convergence" fails because coherent misinformation exists. A static principle of "reject surprise" fails because discovery exists. A purely textual instruction to "express uncertainty" fails if unsupported claims still become persistent memory or training data.

The proposed alternative is a two-stage discipline. **Inversion** produces a candidate relational state that might resist superficial variations in language. **Doubt** asks whether that candidate deserves an assertion, a durable memory record, or a parameter update. Where the evidence is inadequate, the candidate is neither believed nor destroyed: it is retained as a versioned unresolved hypothesis. Where external evidence changes, the record changes with it. In mathematical terms the aim is not maximum contraction of latent variance but calibrated, recoverable movement among representational and epistemic states.

One might call this a *right to remain unresolved*. It is not a model's moral right or an indication of sentience; it is an engineered property of its knowledge-management process. Its practical value can be assessed through true-discovery recall, false-promotion rates, corrections after restart, and resource-aware investigation. The resulting system could be less eloquent about doubt but more effective at respecting it. That would be progress.

# Conclusion

*Inversion Is All You Need* proposed that relational invariants should have a first-class dynamical representation inside transformers. *Doubt Is All You Need!* proposes that a candidate invariant should not automatically become a confident claim, persistent fact, or gradient target. A deliberately engineered invariant space needs an equally deliberate **commitment protocol**: novelty should remain distinguishable from error, surprise from falsity, retrieval from verification, and numerical coherence from truth.

This paper has specified a model, a ledger, gates, failure cases, and preregisterable experiments, but it has presented **no experimental performance claims**. The most decisive future result would not be a beautiful geometric plot or a model announcing its own self-awareness. It would be a replicated demonstration that an unexpected correct idea can survive uncertainty, gain evidence, revise a prior record, and improve subsequent decisions with an auditable causal trail. If matched simpler methods accomplish the same thing, the proper conclusion is that the new machinery is unnecessary for that task. The gate must protect knowledge without locking discovery outside.

# Acknowledgements and research provenance

The technical background includes Martin Timms's *Invariant-Space-LLM*, OpenGML and BRCT investigations [1–3], alongside exploratory discussions with a locally deployed AI research system referred to as Vishva. Such model-generated discussions are sources of hypotheses and examples, not independent measurements of gate activity or co-authorship. The author is responsible for all proposed mechanisms, factual claims, test design, and interpretation. The research proposal draws inspiration from conversations on cognitive architecture, evidence and uncertainty; inspiration is not experimental validation.

# References

[1] Timms, M. (2026). **Inversion Is All You Need: Dynamic Invariant Spaces for Transformer Language Models.** GitHub research draft, version 0.5.5. <https://github.com/Electro-resonance/Invariant-Space-LLM/blob/main/paper/Inversion_Is_All_You_Need_Dynamic_Invariant_Spaces.md>.

[2] Timms, M. (2026). **Invariant-Space-LLM: `src/invariant_space_layer.py`.** Illustrative PyTorch research prototype. <https://github.com/Electro-resonance/Invariant-Space-LLM/blob/main/src/invariant_space_layer.py>.

[3] Timms, M. (2026). **OpenGML — Open Geometric Music Language.** GitHub project. <https://github.com/Electro-resonance/OpenGML>.

[4] Vaswani, A., et al. (2017). **Attention Is All You Need.** *Advances in Neural Information Processing Systems*, 30. <https://arxiv.org/abs/1706.03762>.

[5] Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). **On Calibration of Modern Neural Networks.** *ICML*, PMLR 70, 1321–1330. <https://proceedings.mlr.press/v70/guo17a.html>.

[6] Kadavath, S., et al. (2022). **Language Models (Mostly) Know What They Know.** arXiv:2207.05221. <https://arxiv.org/abs/2207.05221>.

[7] Geifman, Y., & El-Yaniv, R. (2017). **Selective Classification for Deep Neural Networks.** arXiv:1705.08500. <https://arxiv.org/abs/1705.08500>.

[8] Angelopoulos, A. N., & Bates, S. (2021). **A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification.** arXiv:2107.07511. <https://arxiv.org/abs/2107.07511>.

[9] Lewis, P., et al. (2020). **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.** *NeurIPS*, 33. <https://arxiv.org/abs/2005.11401>.

[10] Lin, S., Hilton, J., & Evans, O. (2022). **TruthfulQA: Measuring How Models Mimic Human Falsehoods.** *ACL*, 3214–3252. <https://aclanthology.org/2022.acl-long.229/>.

[11] Manakul, P., Liusie, A., & Gales, M. (2023). **SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models.** *EMNLP*, 9004–9017. <https://aclanthology.org/2023.emnlp-main.557/>.

[12] Gurnee, W., et al. (2026). **Verbalizable Representations Form a Global Workspace in Language Models.** Transformer Circuits (July 2026). <https://transformer-circuits.pub/2026/workspace/>.

# Appendix A: Minimal event schema

A practical audit record should contain at least the following fields. Any field that is not available should be explicitly null, not inferred from generated prose.

```json
{
  "event_type": "claim_gate_decision",
  "event_id": "host-generated-unique-id",
  "timestamp_utc": "ISO-8601",
  "claim_id": "canonical-proposition-digest",
  "model_checkpoint": "hash-or-version",
  "invariant_workspace_state_hash": "hash-or-null",
  "source_ids": ["immutable-source-reference"],
  "source_versions": ["version-or-valid-time"],
  "scores": {
    "novelty": null,
    "uncertainty": null,
    "contradiction": null,
    "geom_surprise": null,
    "evidence_support": null
  },
  "generation_action": "qualify",
  "memory_old_status": "proposed",
  "memory_new_status": "unresolved",
  "weight_update_allowed": false,
  "decision_rule_version": "dw-experiment-v1",
  "reasons": ["no_independent_source"],
  "human_or_external_attestation": null
}
```

# Appendix B: Reproducibility checklist

A release accompanying the paper should publish the baseline training configuration and checkpoint hashes; the entire gate policy and event schema; synthetic-fact generation seeds; source-provenance metadata and document-level splits; raw outputs and host telemetry; per-arm error and coverage tables; failure cases including false rejects and missed discoveries; statistical test scripts; compute and latency accounting; and the exact code paths used to disable DIS, GG, MG and LG. Experimental claims should be explicitly marked *not yet tested* until the corresponding artefacts are available.

# Appendix C: Decision table for irreversible commitments

| Candidate state | Generate? | Store? | Update weights? |
|:--|:--|:--|:--|
| Open hypothesis, no evidence | Yes, labelled speculative | Yes, unresolved partition | No |
| Independently corroborated, scoped fact | Yes, cite support | Yes, supported with metadata | Only after explicit separate test |
| Source contradiction, unresolved | Present conflict accurately | Yes, under review | No |
| Demonstrably forged citation | Correct or reject citation | Preserve event for audit, not as truth | No |
| Updated authoritative evidence | Present revised conclusion | Preserve old + new versions | Optional authorised learning only |

This decision table is an intended policy, not a claim about the behaviour of an existing BRCT v0.3.8 or v4.x runtime.
