---
name: dialectical-source-quality-admiralty
description: Use when evaluating whether research evidence supports a claim, to systematically rate source reliability, separate it from claim credibility, and identify missing evidence
---

# Dialectical Source Quality: Admiralty Scale

## Overview

Not all sources are equal. A tweet from a CEO has different weight than a peer-reviewed study. But even trustworthy sources can misapply evidence, and even questionable sources can state facts correctly.

This skill adapts the **Admiralty Scale** (intelligence community's source-rating system) to evaluate:
1. **Source reliability** (Can this source be trusted?)
2. **Claim credibility** (Does this source actually support THIS specific claim?)
3. **What evidence is missing** to conclusively prove or disprove

This skill pairs with **dialectical-challenge**, which uses it to stress-test whether conclusions are actually supported by their evidence base.

## When to Use

- Evaluating whether research evidence supports a strategic claim
- Deciding which sources to prioritize when evidence conflicts
- Identifying gaps: "What would we need to see to actually prove this?"
- Auditing an analysis: "Are we citing sources correctly?"
- Weighting competing claims when you have limited evidence

**Do NOT use for:**
- Obvious fact-checking (use primary sources directly)
- Real-time journalism (Admiralty scale assumes stable sources; breaking news sources are unstable)

## The Admiralty Scale Adapted

**Source Reliability Ratings** (Is the source trustworthy?):

| Rating | Definition | Examples | Bright Line |
|--------|-----------|----------|------------|
| **A** | Completely reliable (consistently accurate, verifiable, no conflicts of interest) | Peer-reviewed academic research, government statistical agencies, transparent methodologies | Methodology is public; results can be independently verified; no incentive to distort |
| **B** | Usually reliable (generally accurate, some methods opaque or minor conflicts of interest) | Reputable news organizations, established research firms, domain experts | Methodology is mostly transparent; track record is good; conflicts are disclosed or minor |
| **C** | Fairly reliable (mixed track record, some credibility issues, potential biases) | Industry consultancies, analyst firms with client bias, subject-matter experts with incentive misalignment | Methodology is opaque; conflicts of interest are structural; some past inaccuracies |
| **D** | Unreliable (frequent inaccuracy, high conflicts of interest, poor methodology, unverifiable) | Social media claims, anonymous sources, commissioned research defending specific outcomes, incentive-driven narratives | Unverifiable claims; strong financial incentive to lie; no methodology disclosed |
| **E** | Completely unreliable (proven dishonest, no verifiable basis, obvious propaganda) | Obvious fabrications, known fraudsters, disproven sources | Previously caught lying; claims demonstrably false; no plausible mechanism

**Claim Credibility Ratings** (Does this source actually support THIS claim?):

| Rating | Definition | What to Expect |
|--------|-----------|-----------------|
| **1** | Confirmed (multiple independent A/B sources agree; causal mechanism proven) | Fact is established beyond reasonable doubt |
| **2** | Probably true (A/B sources agree; mechanism clear; some evidence supporting) | Likely accurate but not definitive |
| **3** | Possibly true (B/C sources discuss; plausible mechanism; some contradictory evidence) | Credible but unproven; needs more evidence |
| **4** | Doubtful (single source or low-grade sources; weak mechanism; conflicting evidence) | Claim exists but weak support; alternative explanations possible |
| **5** | Improbable (rare sources; implausible mechanism; significant contradictory evidence) | Unlikely to be true given available evidence |
| **6** | Unconfirmed (no credible sources; no mechanism stated; no supporting evidence) | Cannot assess credibility from available data |

**Combined Rating Format**: A-1, B-3, C-2, D-4, etc.

## 3-Step Evaluation Process

### Step 1: Rate Source Reliability (A-E)

For each source, assess:

| Factor | High Reliability (A-B) | Low Reliability (C-E) |
|--------|----------------------|----------------------|
| Methodology | Transparent, verifiable | Opaque or unverifiable |
| Track record | History of accuracy | History of inaccuracy or bias |
| Conflict of interest | None or disclosed | Unstated or primary motivation |
| Funding source | Independent or transparent | Commissioned for specific outcome |
| Reputation | Peer-vetted or established | Self-published or fringe |
| Verifiability | Claims can be checked | Claims assumed, not supported |

**Key insight**: Incentive alignment is the strongest predictor of reliability. A recruiter claiming "AI skill shortage" has structural incentive to overstate. A recruiter claiming "AI skills are abundant" would be credible because they'd be fighting their incentive.

### Step 2: Rate Claim Credibility (1-6)

For the specific claim you're evaluating, ask:

1. **Does this source directly address the claim, or only tangentially?**
   - Direct: Source explicitly discusses this specific causal relationship
   - Tangential: Source discusses adjacent topic and you're inferring

2. **Does this source prove the claim or only suggest it?**
   - Proves: Multiple sources agree; mechanism explained; causal direction established
   - Suggests: Single source discusses pattern; causation assumed, not proven

3. **What alternative explanations does the source rule out?**
   - Strong source: Explicitly tests alternatives (e.g., "we controlled for X, Y, Z")
   - Weak source: Assumes its explanation without testing alternatives

4. **Is causation or just correlation shown?**
   - Causal: Temporal sequence established; confounders controlled for; mechanism explained
   - Correlation: Patterns observed; direction ambiguous; confounders unaddressed

5. **Is the evidence recent and stable, or outdated/changing?**
   - Recent: Data within 1-2 years for fast-moving topics; methodology unchanged
   - Stale: Old data; field has evolved; sources contradict newer findings

**Output for Claim Credibility:**

```
Claim: [Specific claim]
Source: [Source name]
Rating: [A-E]-[1-6]

Direct/Tangential: [assessment]
Proves/Suggests: [assessment]
Alternative explanations ruled out: [list]
Causal/Correlation: [assessment]
Recency: [assessment]
```

### Handling Conflicting Sources

When two sources disagree on the same claim:

1. **Compare reliability ratings** (A-E). Higher reliability wins *unless* both are A/B rated.
2. **If equal reliability**: Look at claim credibility (1-6). Lower number (more credible) wins.
3. **If still equal**: Determine *why* they disagree. Different measurements? Time periods? Populations?
4. **Never average ratings**. Instead, identify which methodology is stronger and why.
5. **When both A-2 sources conflict**: That's a finding in itself. Their disagreement signals missing evidence.

Example: If Stanford (A-2) and Gartner (B-2) disagree on whether labor shortage or capability drives AI adoption, don't average to "probably true." Instead: Both factors matter; determine which has more causal weight.

### Step 3: Identify Missing Evidence

For every claim, identify the **minimal evidence** that would elevate credibility:

**If claim is rated 4-6 (doubtful/improbable):**
- What source type would strengthen this? (e.g., "Need: C-level executive testimony on causation" or "Need: time-series data showing labor shortage precedes adoption")
- What test would disprove it? (e.g., "If company without labor shortage adopts AI at same rate, claim fails")

**If claim is rated 1-3 (confirmed/probably true):**
- What evidence would challenge it? (e.g., "Alternative hypothesis: X confound not yet tested")
- What methodology gap exists? (e.g., "Source shows correlation; need causal isolation")

## Template: Source Quality Assessment

```markdown
# Claim: [State the specific claim]

## Evidence Sources

| Source | Type | Reliability (A-E) | Claim Rating (1-6) | Support? |
|--------|------|-------------------|-------------------|----------|
| [Name] | [Type] | | | Proves/Suggests/Contradicts |
| [Name] | [Type] | | | Proves/Suggests/Contradicts |

## Aggregate Credibility Assessment

**Combined rating**: [e.g., "Consensus B-3: probably true but unproven causation"]

**Strongest evidence**: [What source best supports this?]

**Weakest link**: [What's missing or contradicted?]

## Missing Evidence

What would conclusively prove/disprove this claim?

- **Source type needed**: [e.g., "Longitudinal hiring data showing temporal sequence"]
- **Methodology needed**: [e.g., "Randomized experiment comparing treatment vs. control"]
- **Evidence type needed**: [e.g., "Executive testimony on actual decision-making"]

## Conflicts in Evidence

If sources disagree:

| Claim Aspect | Source A Says | Source B Says | Resolution |
|-------------|---|---|---|
| | | | Which is more credible and why? |
```

## Common Mistakes

**❌ Confusing source credibility with claim credibility**
- Mistake: "Stanford is A-rated, so their claim about AI adoption must be 1-rated"
- Reality: Stanford could publish an A-rated study about a phenomenon they only correlate, not explain causally
- Fix: Rate source reliability separately from what the source actually claims about THIS specific claim

**❌ Overlooking incentive bias**
- Mistake: Treating a consultant's AI report same as peer review
- Reality: Consultant profits from recommending AI; peer review does not
- Fix: Make incentive alignment explicit. Use the contrast test: "Would this source make the opposite claim if incentives reversed?"

**❌ Assuming recent = reliable**
- Mistake: "2024 report must be better than 2020 research"
- Reality: Recency helps with stability (field may have changed), but doesn't guarantee methodology quality
- Fix: Separate recency from methodology quality. A rigorous 2020 study beats a sloppy 2024 blog post.

**❌ Rating based on intuition ("feels credible")**
- Mistake: Not systematically evaluating methodology, track record, conflicts
- Fix: Use the rubric. If a source "feels credible," identify why: methodology? track record? lack of conflicts?

**❌ Failing to identify missing evidence**
- Mistake: Declaring claim "proven" without asking what evidence would disprove it
- Fix: For every claim, explicitly state: "This would be disproven if [X observation occurred]"

## Real-World Impact

This structure prevents:
- Over-reliance on convenient but weak sources
- Mistaking correlation for causation in cited research
- Missing obvious gaps in evidence
- Uncritical acceptance of sources with misaligned incentives
- False confidence when evidence is actually weak

It enables:
- Rapid prioritization of which sources matter most
- Clear identification of what needs testing next
- Honest assessment: "We have B-3 support; this is unproven"
- Efficient refutation: "This claim is D-5; here's what would change that"

---

See also: **dialectical-challenge** (which invokes this skill), **dialectical-alternative-hypotheses** (for generating competing explanations), **dialectical-causal-chain** (for analyzing step-by-step logic)
