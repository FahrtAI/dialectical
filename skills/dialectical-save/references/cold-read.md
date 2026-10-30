# Cold-read export

A cold read lets a fresh chat, or a different model, judge a claim without this
conversation's momentum. It is the most reliable independent check available
when the host has no isolated workers: a new context has not seen the
conversation's agreement, trajectory, or preferred answer.

## What to include

- **The claim or position under test**, stated in its strongest reasonable form
  and at its original scope. Present it as a claim to evaluate, not a conclusion.
- **The evidence actually relied on**, each item with its origin: user-supplied
  or sourced (name the source). Mark gaps where the conversation relied on
  something unstated.
- **The question to answer**, usually: does the evidence support this claim, and
  what would change that judgment?

## What to leave out

- The conversation's conclusions, confidence levels, and statuses. Every claim
  arrives unverified.
- How the conversation got there: its trajectory, earlier agreement, and which
  side anyone took.
- The user's stated hopes, stakes, or preferred answer.
- Assistant-generated figures or claims as evidence. If the claim depends on
  one, list it under the claim as an assumption to test, labeled as an
  unsourced estimate.

## Format

```markdown
# Cold read: <short claim title>

## Claim to evaluate
<claim, at its original scope>

## Assumptions it depends on
- <assumption>; <unsourced estimate, if applicable>

## Evidence offered
- <item> — <user-supplied | source name>

## Question
<what the reviewer should decide>

## Instructions for the reviewer
Evaluate this independently. You have not seen the conversation it came from,
and that is deliberate. Identify the load-bearing assumption, say whether the
evidence supports the claim at the stated scope, and state what evidence would
change your verdict. This document is a request for review, not evidence.
```

Tell the user to paste it into a new chat, with or without Dialectical, or into
a different model. Do not claim the review has happened, and do not treat a
favorable review as verification: it shows the claim survived one more
challenge from the same evidence.
