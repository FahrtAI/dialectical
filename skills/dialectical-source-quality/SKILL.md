---
name: dialectical-source-quality
description: Rate how reliable sources are and how credible the information they provide is, separately, using the Admiralty scale, and identify missing evidence. Use when the user asks how much weight particular sources or pieces of evidence deserve; do not use for broad exploration (RESEARCH) or to settle one proposition (VERIFY).
metadata:
  version: "0.7.0"
---

# Source Quality

Assess how much weight evidence deserves by rating its source and its content independently.

Use the shortest complete response that preserves source independence,
proposition fit, uncertainty, and the distinction between reliability and
information credibility. For a clear ordinary-language invocation that does
not name SOURCE-QUALITY, begin with one line:
`SOURCE-QUALITY — <brief context-specific description>.` Omit the cue for an
explicit command, mere discussion, or internal technique. Ratings do not
automatically settle the underlying claim.

The Admiralty scale uses two independent ratings, written together as `B2`:

| Source reliability | | Information credibility | |
|---|---|---|---|
| A | Completely reliable | 1 | Confirmed by independent sources |
| B | Usually reliable | 2 | Probably true |
| C | Fairly reliable | 3 | Possibly true |
| D | Not usually reliable | 4 | Doubtful |
| E | Unreliable | 5 | Improbable |
| F | Reliability cannot be judged | 6 | Truth cannot be judged |

F and 6 mean there is not enough basis to rate. They are not the bottom of the scale; never rank them below E or 5.

## Operation

1. State the specific claim the evidence is meant to support. Rate evidence against that claim, not the general topic.
2. List the sources actually consulted, and rate only those. If a source is known only from memory, from the user's description, or from another source's account of it, label the rating accordingly.
3. Rate source reliability (A–F) from the source's record on this kind of information: past accuracy, transparency of method, access to what it reports, and incentives to distort. Do not assign a grade from source type alone; a peer-reviewed paper or a major outlet can be wrong on a given subject. Reserve A for a long, checked record on this kind of information. Use F when there is no basis to judge.
4. Rate information credibility (1–6) from the content, independently of the source grade: corroboration, consistency with what is otherwise known, internal coherence, and plausibility. A reliable source can report doubtful information, and an unreliable source can report confirmed information. A statement against a source's apparent interest can be informative about incentives, but it is not an automatic credibility upgrade: consider whether the source could know, other incentives, framing, and independent corroboration. Apply the same scrutiny to self-serving information.
5. Check independence before counting corroboration. Reports that trace back to one original source, dataset, or press release count once.
6. Note what the information actually shows for this claim: direct or tangential, correlation or causation, and whether it is current enough for the subject.
7. When sources conflict, identify why (different measures, populations, periods, or methods) before preferring one. Do not average ratings or resolve a conflict mechanically by grade. A conflict between strong sources is itself a finding.
8. Identify the missing evidence that would most raise or lower credibility, and the observation that would refute the claim.

## Output

For each source, give its rating (for example `C3`) and a one-line basis. Then give the overall assessment of the claim in words, the conflicts and shared origins found, and the missing evidence. A fuller template is in [`references/template.md`](references/template.md).

## Delegation

When several substantial sources can be assessed independently and the host supports isolated workers, assign one bounded source assessment per worker. Give every worker the same specific claim and rating definitions, and require it to distinguish direct inspection from secondhand knowledge. The conversational agent audits shared origins, calibrates ratings across sources, resolves conflicts, and owns the overall assessment. Do not delegate a single short assessment merely to multiply opinions.

## Boundaries

- Do not rate a source that was not consulted as if it had been read.
- Do not let a source's grade stand in for the credibility of a specific claim, or the reverse.
- Do not treat "cannot be judged" as unreliable or false.
- Do not call a claim confirmed when its corroboration traces to one origin.
- Do not search for new sources unless asked; that is RESEARCH. Do not deliver a verdict on one proposition; that is VERIFY.
