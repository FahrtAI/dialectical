# Causal chain template and example

## Template

```markdown
# [Claim]

## Chain as stated

A → B → C → outcome

## Assumptions

| Link | Assumption | Kind | If false | Criticality |
|---|---|---|---|---|
| A → B | | Priority / Necessity / Direction / Transfer / Timing / Barriers | | Linchpin / Load-bearing / Minor |

## Link tests

| Link | Mechanism stated? | Causation shown or assumed? | Other paths? | Possible confounder | What would show it false |
|---|---|---|---|---|---|

## Verdict

- **Solid / Vulnerable / Brittle**
- **Basis:** [which links were checked against evidence; which rest on assumption]
- **Weakest link:**
- **Scope:** [outcome, magnitude, and timing actually supported]
- **Alternative paths:** [whether any supported path suffices; no unique linchpin does not imply Solid]
- **Evidence that would settle it:**
```

## Example

Claim: "Launching a self-service help center will cut support tickets in half next year. Customers will search it, find answers, and stop filing tickets."

Chain as stated: launch → customers search the help center → customers find answers → customers don't file tickets → ticket volume halves.

| Link | Assumption | Kind | If false | Criticality |
|---|---|---|---|---|
| Launch → search | Customers try the help center before filing | Barriers | Fewer customers search on their own, but article suggestions in the ticket form still reach them | Load-bearing |
| Search → answers | At least half of tickets ask questions an article can answer | Necessity | Account-specific issues such as billing errors and bugs still need an agent, so tickets cannot halve | Linchpin |
| Answers → no ticket | Customers who find an answer don't file anyway | Barriers | Some file to confirm; the reduction shrinks | Load-bearing |
| Whole chain | Articles cover the top topics within the year | Timing | The reduction arrives later than claimed | Minor |

Only one assumption is a linchpin. The others weaken the result but leave a route to it.

Verdict: **Vulnerable.** The linchpin is unexamined; nobody has checked what share of tickets an article could answer. Tagging a sample of last quarter's tickets as article-answerable or not would settle it. If fewer than half are, the claim fails even with perfect deflection.
