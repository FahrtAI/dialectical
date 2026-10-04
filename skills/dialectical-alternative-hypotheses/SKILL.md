---
name: dialectical-alternative-hypotheses
description: Use when you need to systematically generate competing explanations for an observation, to identify which alternative is most likely and what evidence would eliminate each
---

# Dialectical Alternative Hypotheses

## Overview

When you observe a pattern (webinar attendees convert 3x more, AI adoption is accelerating), the natural hypothesis is tempting but incomplete. This skill provides a **systematic method to generate all plausible alternatives**, then rank them and identify which is most fragile to evidence.

This skill pairs with **dialectical-challenge**, which invokes it to test whether the primary hypothesis is actually correct, or whether competing explanations better account for the data.

## When to Use

- Testing observed correlations ("X is rising when Y is rising—why?")
- Evaluating causal claims ("We believe X caused Y because...")
- Choosing between competing explanations when data is ambiguous
- Identifying which hypothesis is easiest to disprove
- Building exhaustive Analysis of Competing Hypotheses (ACH) matrices

**Do NOT use for:**
- Single-cause phenomena (genuinely only one explanation fits)
- Purely speculative "what-if" scenarios (needs real observations to explain)

## The 4-Category Confounding Framework

Instead of brainstorming alternatives freely, systematically enumerate them by confounding type:

### Category 1: Selection/Composition Bias
**Question**: Are the groups actually comparable, or are they pre-sorted?

Examples of this confound:
- Webinar attendees are already pre-qualified (self-selected to show up)
- Companies that adopt AI were always more innovative
- High performers were always ambitious before the program

**Method**: Ask "What pre-existing characteristics differ between groups?"

### Category 2: Treatment Intensity Bias
**Question**: Is the difference in outcome caused by the observed event, or by *differential treatment after* the event?

Examples:
- Webinar attendees receive more aggressive sales follow-up
- Promoted employees get more mentorship and challenging assignments
- Early AI adopters get more vendor support and consulting

**Method**: Ask "Do the groups receive different intensity of treatment after the observation?"

### Category 3: Measurement/Signal Artifact
**Question**: Does the observation measure what we think, or is it a signal of something else?

Examples:
- "Webinar attendance" signals timing readiness, not persuasion
- "High engagement" signals someone in buying mode, not quality lead
- "Early adoption" signals company maturity/resources, not product quality

**Method**: Ask "What does this behavior *signal* about pre-existing state?"

### Category 4: Comparison Group Contamination
**Question**: Is the control group actually a valid comparison, or diluted/misaligned?

Examples:
- Non-attendees include tire-kickers and cold prospects (not just people who chose not to attend)
- Comparison companies are smaller/less mature (different baseline)
- Control group defined differently than treatment group

**Method**: Ask "How do the groups differ in composition and inclusion criteria?"

## 5-Step Generation Process

### Step 1: State the Observation Precisely

What's actually observed? Be specific about measurement, scale, and comparison.

❌ Vague: "Webinars work"
✅ Precise: "Enterprise prospects who attend one webinar convert at 3x the rate of those who don't attend"

### Step 2: State the Primary Hypothesis

What's the current explanation?

Example: "Webinars are effective because they build trust and demonstrate expertise"

### Step 3: Generate Alternatives by Confounding Type

Using the 4-category framework, generate at least one alternative per category:

**Selection bias**: Attendees were already 3x more likely to buy (self-selected)
**Treatment intensity**: Attendees receive more sales follow-up (escalation effect)
**Measurement signal**: Attendance signals company is in buying mode right now (timing)
**Comparison group**: Non-attendees diluted with cold/unqualified leads (mixed pools)

### Step 4: Test Falsifiability for Each

For each hypothesis, ask: "What's the **minimal evidence** that would disprove this?"

| Alternative | Disproved By |
|-------------|-------------|
| Selection bias | Pre-webinar engagement data showing attendees were already 3x engaged |
| Treatment intensity | Activity logs showing identical post-event follow-up |
| Measurement signal | Identical conversion rates for identical prospects contacted 2 weeks later |
| Comparison group | Matched comparison (cold prospects w/ similar qualification at start) |

### Step 5: Rank by Likelihood & Fragility

**Likelihood ranking**: Which alternative best explains the observed pattern?
**Fragility ranking**: Which would be easiest/cheapest to disprove?

| Hypothesis | Likelihood | Evidence Cost to Disprove | Verdict |
|-----------|-----------|--------------------------|---------|
| Primary (Webinars persuade) | Moderate | High (need counterfactual) | Keep testing |
| Selection bias | High | Low (engagement logs) | Easy kill |
| Treatment intensity | High | Low (activity logs) | Easy kill |

**Key insight**: Hypotheses that are easy to falsify but haven't been yet are MORE credible, not less. If selection bias would be disproved by 30 seconds of data-checking and hasn't been checked, that's a gap.

**How many alternatives is enough?**
- **Minimum**: At least one alternative per confounding category (4 total)
- **Sufficient**: 6–10 distinct alternatives covering different mechanisms
- **Overdone**: 15+ alternatives where many are unlikely or redundant variations
- **Signal you're done**: When new alternatives are just restatements of earlier ones, or require unrealistic explanations (e.g., "cosmic interference")

**When all alternatives are equally plausible:**
If multiple hypotheses rank equally high (all "HIGH" likelihood, all similar fragility), design a test that *distinguishes* between them. Example: If selection bias and follow-up intensity both seem plausible and hard to disprove, run experiment with two groups: (1) attendees with normal follow-up, (2) non-attendees with *equal* follow-up intensity. Result disconfirms follow-up intensity hypothesis, leaving selection bias.

## Template: Alternative Hypothesis Matrix

```markdown
# Observation: [State precisely]

## Primary Hypothesis
[Current explanation and why it's believed]

## Alternative Hypotheses by Confounding Type

### Selection/Composition Bias
- **Alternative**: [What pre-existing difference could explain this?]
- **Mechanism**: [How would this produce the observed pattern?]
- **Disproved by**: [What evidence would eliminate this?]

### Treatment Intensity Bias
- **Alternative**: [What differential treatment could explain this?]
- **Mechanism**: [How would this produce the observed pattern?]
- **Disproved by**: [What evidence would eliminate this?]

### Measurement/Signal Artifact
- **Alternative**: [What does this behavior signal about pre-existing state?]
- **Mechanism**: [How would this produce the observed pattern?]
- **Disproved by**: [What evidence would eliminate this?]

### Comparison Group Contamination
- **Alternative**: [How are the comparison groups actually different?]
- **Mechanism**: [How would this produce the observed pattern?]
- **Disproved by**: [What evidence would eliminate this?]

## Ranking

| Hypothesis | Likelihood | Fragility | Next Test |
|-----------|-----------|-----------|-----------|
| | High/Medium/Low | Easy/Hard | |

## Highest-Priority Disconfirmation Test
[Which single test would eliminate the most dangerous competing hypothesis?]
```

## Common Mistakes

**❌ Generating "alternatives" that aren't actually alternatives**
- Observation: "Women earn less in tech"
- Bad alternative: "This is because of resume quality" (not an alternative if you don't control for resume)
- Good alternative: "Pre-hiring screening filters for different experience levels between genders"

**Fix**: Each alternative must explain the same observation with a different causal mechanism.

**❌ Ranking by intuition instead of evidence cost**
- Mistake: "This alternative seems unlikely" without asking what would prove it false
- Fix: Use evidence cost + plausibility, not gut feel

**❌ Not recognizing that high-likelihood alternatives are still threats**
- Mistake: "Selection bias is so obvious, we don't need to check"
- Reality: If it's obvious and not checked, it's undermining your conclusion
- Fix: Treat high-likelihood alternatives as highest-priority to test

**❌ Generating alternatives that can never be disproven**
- Bad: "Maybe it's unknowable cosmic forces"
- Good: "Maybe buyers self-select into the webinar cohort based on pre-existing sophistication"
- Fix: Every alternative must be testable

**❌ Assuming the primary hypothesis is true, then generating alternatives**
- Mistake: Starting with "Webinars work, so what else might also explain this?"
- Fix: Treat all hypotheses (including primary) equally. Rank by evidence, not by which was stated first.

## Real-World Impact

This structure prevents:
- False conclusions from unexamined confounds
- Wasted resources testing hypotheses when easier disconfirmation exists
- Overconfidence in weak causal claims
- Analysis that ignores the most dangerous competing explanations

It enables:
- Efficient prioritization of what to test next
- Clear separation between "seems likely" and "is actually supported"
- Fast identification of which competing hypothesis is most fragile

---

See also: **dialectical-challenge** (which invokes this skill), **dialectical-causal-chain** (for analyzing step-by-step logic), **dialectical-source-quality-admiralty** (for evaluating evidence quality)
