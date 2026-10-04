---
name: dialectical-causal-chain
description: Use when analyzing logical chains of reasoning where each step depends on previous ones, to identify assumptions that would break the entire argument if false
---

# Dialectical Causal Chain

## Overview

A causal chain is a sequence of steps: A causes B, B requires C, C leads to D. This skill provides a systematic method to decompose chains, test each link, and identify **linchpin assumptions**—unstated premises that, if false, collapse the entire chain.

This skill pairs with `dialectical-challenge`, which can invoke it to stress-test causal logic.

## When to Use

- Analyzing strategic arguments ("Market growth will accelerate because X → Y → Z")
- Evaluating policy chains ("Regulation A → B happens → C results")
- Testing business logic ("Customer problem → market gap → product opportunity → adoption")
- Checking research claims ("Cause X observed → Y must be true")
- Finding vulnerabilities in reasoning before committing resources

**Do NOT use for:**
- Simple correlations (no steps involved)
- Linear sequences without dependencies (Step A, then Step B, but B doesn't depend on A working)

## Core Method: The 5-Step Decomposition

### Step 1: Map the Explicit Chain

Write out each causal step using this format:

```
Step 1 → Step 2: [condition needed] → Step 3: [condition needed]
```

Be literal. If the claim is "market pressure drives automation drives AI adoption," write exactly that, not a cleaned-up version.

### Step 2: Identify ALL Assumptions at Each Link

For each arrow (→), ask: "What must be true for this to work?"

Examples:

| Link | Assumption |
|------|-----------|
| Market pressure → Automation | Market pressure is primary driver (not regulation, competition, or strategy) |
| Automation → AI (not RPA) | Automation inherently requires AI (vs. cheaper alternatives) |
| Infrastructure → Widespread adoption | Having infrastructure removes adoption barriers |

**Common assumption categories:**
- **Priority**: This is the main reason (not secondary)
- **Technology choice**: This tool/method is necessary (not alternative approaches)
- **Causation direction**: A causes B, not reverse or both driven by C
- **Scale transfer**: What works in one domain works across domains
- **Timing**: Steps occur in this order
- **Barriers removed**: Completing earlier steps removes obstacles to later ones

### Step 3: Classify Assumptions by Criticality

For each assumption, ask: "If this is false, does the entire chain fail?"

**Linchpin assumptions** (chain-breakers): If false, everything downstream collapses.

**Load-bearing assumptions** (weakens chain): If false, the chain is possible but much less likely.

**Minor assumptions** (vulnerabilities): If false, one link weakens but other paths might remain.

| Assumption | If False | Criticality |
|-----------|----------|------------|
| Market pressure is PRIMARY driver | Hospitals cut staff instead of automating | Linchpin |
| Admin automation REQUIRES AI | RPA solves it cheaper | Linchpin |
| Infrastructure → wider adoption | Hospitals don't adopt beyond admin use | Linchpin |
| Financial ROI is positive | Investment doesn't pay out | Load-bearing |

### Step 4: Test Each Link for Gaps

For each step, ask:

1. **Is the causation claimed or proven?** (Does the chain state it as fact or assumption?)
2. **Are there alternative paths to the same outcome?** (Could Step 2 happen without Step 1?)
3. **Are there confounders?** (Could a third factor cause both Step 1 and Step 2, making the link spurious?)
4. **Is the mechanism stated or hidden?** (Does the chain explain *why* A leads to B, or just assert it?)
5. **What evidence would disprove this link?** (What observation would show it's false?)

### Step 5: Identify the Weakest Link

Rank links by fragility. The chain is only as strong as its weakest assumed link.

**Output format:**

```
Strongest link: [step] (because: [reason])
Weakest link: [step] (because: [reason])
Chain verdict: SOLID / VULNERABLE / BRITTLE
```

## Template: Causal Chain Decomposition

Use this template when analyzing any chain:

```markdown
# [Claim Name]

## Explicit Chain
[Map steps]

## Assumptions by Link
| Link | Assumption | Category | Criticality |
|------|-----------|----------|------------|
| → | | Priority/Technology/Causation/Scale/Barriers | Linchpin/Load-bearing/Minor |

## Linchpin Assumptions (Chain-Breakers)
- **[Assumption 1]**: If false, [what fails]
- **[Assumption 2]**: If false, [what fails]

## Gaps & Vulnerabilities
| Gap | Location | Risk |
|-----|----------|------|
| | | |

## Weakest Links
1. [Link]: [why fragile]
2. [Link]: [why fragile]

## Chain Verdict
- Solid / Vulnerable / Brittle
- Reason: [explanation]
- Evidence that would disprove: [what observation breaks it]
```

## Edge Cases

**Circular causation (A→B→A):**
If the chain loops back, you have a reinforcement cycle, not a linear chain. Example: "Poor customer experience → churn → reduced resources → worse experience → more churn."

Treatment: Identify which step in the loop is the *initial trigger* (exogenous shock). That's where the chain starts. Analyze forward from there. Linchpin assumption: Is the first step strong enough to generate the feedback loop?

**Competing causal chains:**
If multiple pathways lead to the same outcome ("Market pressure *or* regulation *or* competitive pressure could each drive automation"), analyze each chain separately. The outcome is overdetermined (multiple causes sufficient). Key question: Which cause is actually operating?

**Temporal ambiguity:**
When the chain doesn't specify timing ("Pressure → Automation → Infrastructure"), ask: Does each step take weeks or years? Do they overlap? Temporal sequence matters. If Infrastructure takes 2 years and widespread adoption happens in 1 year, the chain is false.

## Common Mistakes

**❌ Conflating correlation with causation**
- Claim: "Hospitals automate because of labor shortage"
- Mistake: Not asking whether labor shortage *precedes* or *follows* automation decisions
- Fix: Establish temporal sequence. Does shortage come first, or does automation create demand for new skills?

**❌ Skipping the mechanism**
- Chain step: "Infrastructure → widespread adoption"
- Mistake: Assuming infrastructure automatically enables adoption
- Fix: What specific mechanism transfers capability? Cultural momentum? Technical capability? Economics? Regulatory change?

**❌ Not questioning assumptions because they "seem obvious"**
- Assumption: "AI automation requires AI infrastructure"
- Mistake: Not considering RPA, rules-based systems, vendor solutions
- Fix: For every assumption, ask what simpler alternatives exist

**❌ Treating all assumptions equally**
- Mistake: Noting 20 assumptions without distinguishing which would actually break the chain
- Fix: Ruthlessly identify linchpin assumptions. Most assumptions are secondary.

**❌ Failing to identify alternative pathways**
- Mistake: Analyzing only the stated chain
- Fix: For each step, ask "what else could cause this outcome?" Those alternatives may break the chain.

**❌ Ignoring temporal constraints**
- Mistake: Assuming steps happen in sequence without checking if the timeline is realistic
- Fix: For each link, ask: How long does this step take? Do the timings add up to the claimed outcome speed?

## Real-World Impact

Without this structure, strategic reasoning devolves into narrative. With it, you can:
- Identify where arguments are bulletproof vs. brittle
- Find which assumptions need evidence vs. which are load-bearing
- Quickly see why competing claims fail or succeed
- Feed key findings to `dialectical-alternative-hypotheses` for alternative-pathway testing

---

See also: **dialectical-challenge** (which invokes this skill), **dialectical-alternative-hypotheses** (for testing alternative causal pathways)
