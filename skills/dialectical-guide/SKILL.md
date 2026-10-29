---
name: dialectical-guide
description: Rank three useful Dialectical commands for the current conversational state and offer MORE for the complete catalog. Use when the user invokes GUIDE or asks which Dialectical command would help now; do not monitor later turns or perform a recommendation before selection.
metadata:
  version: "0.8.0"
---

# Guide

Help the user choose a useful move without taking over the conversation.
GUIDE is invoked on demand; it is not a background mode or observer.

Use the shortest complete menu and rationale the command contract permits. Preserve
disputed premises and uncertainty when explaining why a command fits; ranking
commands does not rank claims or explanations as true. For a clear
ordinary-language invocation that does not name GUIDE, begin with one line:
`GUIDE — Ranking useful commands for here.` Do not add the cue for explicit
GUIDE, mere discussion, or orientation material.

## Operation

1. Review the inquiry's current state using only available context: what the
   user is trying to understand or decide, the claims and alternatives in play,
   the evidence already available, and the present obstacle.
2. Choose the three commands that would be most useful now and rank them from
   most to least useful. Each must address a concrete present need. The ranking
   expresses preference; it is not a sequence and all three are recommendations.
   Do not include GUIDE among its own recommendations.
3. Read the canonical catalog in
   [`../dialectical/references/help.md`](../dialectical/references/help.md) and
   use each selected command's five-word description exactly. Do not invent a
   competing description or catalog.
4. Present the three choices and `[MORE] Show all commands`. Do not perform any
   selected operation in this response.
5. On the user's next turn:
   - a choice of `1`, `2`, or `3` authorizes only the command at that position
     in the most recent GUIDE menu;
   - a named command authorizes only that command;
   - `MORE` returns the complete canonical command catalog from the help
     reference without running anything; after that, wait for a named command;
   - ignoring the menu and continuing the discussion authorizes nothing.
6. If the available context is too thin to rank commands responsibly, ask one
   brief question about what the user wants from the conversation. After the
   answer, provide the ranked three rather than another intake sequence.

Use these distinctions when ranking:

- use RELEVANCE for unclear purpose or scope, COLLECTION GAPS for evidence to
  seek, TEST DESIGN for turning claims or gaps into discriminating tests,
  RESEARCH for seeking evidence, INDICATORS for developments to watch, and
  VERIFY for adjudicating one empirical proposition;
- use HYPOTHESIZE when the explanatory space is narrow and ACH when real
  alternatives and evidence are ready to compare;
- use CHALLENGE to stress-test a position, CAUSAL-CHAIN to inspect its causal
  links, and SOURCE-QUALITY to assess a source;
- use RECAP for a compact recap and DISTILL when the intellectual state has
  become difficult to hold; and
- recommend lifecycle or memory operations only when continuity or persistence
  is the user's present need.

## Response shape

Keep the intervention compact:

```text
Based on where we are:

[1] COMMAND — Canonical five-word operation description.
[2] COMMAND — Canonical five-word operation description.
[3] COMMAND — Canonical five-word operation description.

[MORE] Show all commands
```

Use the actual ranked commands. A single short sentence may explain the ranking
when context alone would not make it clear. Do not add a separate recommended
badge: order carries the recommendation.

## Boundaries

- Do not present the three choices as stages, a workflow, or authorization to
  run more than the user's eventual selection.
- Do not execute the recommendation, browse, delegate, persist anything, or
  create monitoring or scheduled work.
- Do not continue evaluating later turns unless GUIDE is invoked again.
- Do not treat an ignored or declined menu as permission to propose another.
- Do not invoke GUIDE recursively. Show the full catalog only when the user
  chooses MORE or separately asks for HELP or the command list.
- Keep GUIDE in the conversational agent; it needs the current conversation and
  creates no background observer.
