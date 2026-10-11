---
name: dialectical-verify
description: Resolve a specific empirical proposition against authoritative external evidence and report a calibrated verdict. Use for targeted factual adjudication; do not use for broad exploration, value judgments, or claims that cannot be empirically settled.
metadata:
  version: "0.7.0"
---

# Verify

Determine what the best available external evidence warrants about a narrowly stated proposition.

Use the shortest complete response that preserves proposition fit, source
independence, evidence limits, and residual uncertainty. For a clear
ordinary-language invocation that does not name VERIFY, begin with one line:
`VERIFY — <brief context-specific description>.` Omit the cue for an explicit
command, mere discussion, or internal technique. Raise or lower confidence only
when the inspected evidence justifies it, and state the basis.

## Operation

1. Convert the focus into a precise, falsifiable proposition while preserving its scope, date, entities, and qualifiers.
2. Identify what evidence would support, refute, or leave the proposition unresolved.
3. Consult primary or otherwise authoritative sources. Use independent corroboration when the claim is consequential, disputed, or vulnerable to source error.
4. Check that each source actually addresses the proposition rather than a nearby claim.
5. Return:
   - **Proposition**
   - **Verdict:** supported, refuted, mixed, or unresolved
   - **Evidence**
   - **Source quality and limitations**
   - **Residual uncertainty**
6. Cite the evidence directly and include relevant dates.

When sources of differing quality bear on the proposition, `dialectical-source-quality` can rate them. Say so when you apply it.

Source assessment is an internal technique for this verification, not a new
objective requiring another consent question. Relevant evidence retrieval is
part of the requested verification. A broader research question or persistence
still needs authorization; naming an additional method does not grant it.

If external evidence cannot be accessed, say that verification was not completed. Offer a verification plan or clearly labeled provisional assessment instead.

## Delegation

For a consequential, disputed, or anchoring-sensitive proposition, default to an isolated evidence worker when the host supports one. Give it the exact proposition, jurisdiction, dates, qualifiers, evidence criteria, and relevant sources or tools; omit unrelated conversational conclusions. When the stakes or source-dependence risk justify it, use a second bounded worker to seek independent corroboration or disconfirmation. The conversational agent checks proposition fit and source independence and owns the verdict. Verify a routine proposition directly when an extra worker would add no meaningful check.

## Boundaries

- Do not turn absence of a located source into proof that an event never occurred.
- Do not use confidence language as a substitute for evidence.
- Do not broaden a narrow proposition midstream without making the change explicit.
- Do not call a claim verified when the evidence is indirect, conflicting, or only repeats the same underlying source.
