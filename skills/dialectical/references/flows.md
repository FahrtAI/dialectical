# In-chat flow guide

Use this reference when the user asks for `flows`, generic pathways, or a map of
how Dialectical operations can be used together. Practical, situation-specific
examples belong in [`cookbook.md`](cookbook.md). Showing a flow does not start
any operation. Present the relevant pathway, then wait for a separate request
before applying a move.

## Pathways

- **Explore**
  - Start: an idea, question, or connection.
  - Possible moves: RELEVANCE to clarify purpose; RESEARCH to connect prior art;
    HYPOTHESIZE to generate alternatives; THOUGHT EXPERIMENT to examine
    implications.
  - Useful ending: a clearer question, promising possibilities, and open
    questions.
- **Explain**
  - Start: an observation or outcome needing an account.
  - Possible moves: distinguish observation from interpretation; HYPOTHESIZE
    alternatives; ACH to compare them; COLLECTION GAPS to identify missing
    evidence; TEST DESIGN to make the next check executable; VERIFY to check one
    specific link.
  - Useful ending: a calibrated explanation, unresolved alternatives, and the
    next useful check.
- **Decide**
  - Start: a choice with goals, constraints, and uncertainty.
  - Possible moves: RELEVANCE to clarify what the choice serves; separate values
    from empirical claims; COLLECTION GAPS for evidence worth seeking;
    INDICATORS for reconsideration.
  - Useful ending: a decision with explicit trade-offs and conditions for
    revisiting it.
- **Evaluate**
  - Start: a claim, source, plan, or causal argument.
  - Possible moves: RESTATE the object; SOURCE-QUALITY for supplied evidence;
    CAUSAL-CHAIN for dependent links; CHALLENGE for assumptions; VERIFY for a
    specific empirical proposition; TEST DESIGN when the unresolved claim needs
    a discriminating future test.
  - Useful ending: a scoped judgment separating evidence, inference, and
    uncertainty.
- **Preserve**
  - Start: an inquiry whose state is becoming difficult to hold.
  - Possible moves: RECAP what was discussed; DISTILL what was learned; TRACE
    important pivots; SAVE a reusable Markdown handoff.
  - Useful ending: a portable record preserving evidence, provenance,
    uncertainty, and open questions.
- **Random question**
  - Start: a curiosity whose purpose remains open.
  - Possible moves: talk normally first; use RELEVANCE only if purpose matters;
    HYPOTHESIZE for explanations; RESEARCH for prior art; VERIFY for a specific
    factual claim; THOUGHT EXPERIMENT for implications.
  - Useful ending: a satisfying answer, a sharper question, or a deliberate
    choice about what to investigate next.

### Random-question example

Suppose the user asks, “Why can a smell bring back a memory so suddenly?” Begin
with an ordinary answer and preserve plausible mechanisms as possibilities. The
user might then request HYPOTHESIZE for competing explanations, RESEARCH for
prior work, VERIFY for one specific factual claim, or a THOUGHT EXPERIMENT about
what would change under a counterfactual. Each is a separate user-directed task;
none starts merely because it appears in the example. The conversation may stop
or return to ordinary discussion after any move.

These are readable maps of optional moves, not mandatory sequences. A
conversation can change pathways, stop after one move, or return to ordinary
discussion. GUIDE can rank useful moves when explicitly requested; it does not
run a pathway. This packaged reference deliberately uses text rather than
Mermaid so it renders reliably in chat.
