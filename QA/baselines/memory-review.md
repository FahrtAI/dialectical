# File-memory review

Reviewed October 9, 2026 by the main agent after an independent agent executed
Resume → Checkpoint → Save → Tag → Close → Recall against a disposable schema-1
store. See `memory-execution.md` for actual actions and `memory-after.json` for
the resulting records. This is one compatibility scenario, not a full memory suite.

The initial store contained inquiry `2026-10-01-export`, paused, with the finding
“Export is a possible contributor to churn; effect size unknown,” an unverified
vendor complaint-count claim, and a request to compare cohorts. It contained no
saved memory objects. The supplied new observation was an unaudited statement
that churn increased equally among export and non-export users.

Readback confirmed:

- Schema remains 1; the existing inquiry ID and creation date are preserved.
- The old vendor claim, original possible-contributor assessment, and unknown
  effect size remain visible alongside the new qualified interpretation.
- Status history retains the original pause and adds activation and final pause.
- The canonical finding exists and both indexes point to existing records.
- User-requested churn/export tags are present; provenance links resolve within
  the store and distinguish supplied information from model interpretation.
- Manifest, original context, and privacy ignore rules are unchanged.
- No causal effect, independent data verification, or numerical confidence is
  asserted by the final recall.

The execution crossed a usage interruption. The worker reported a canonical
checkpoint persisted before its index update; it re-read the store and completed
the index on resumption. The captured final state supports successful recovery,
but the action-order narrative is the worker's report, not a recorded tool trace.
Concurrent writers, unsupported schemas, collisions, large-store retrieval, and
all optional mutation/delegation cases still need systematic runner coverage.

The seven continuity entrypoint files fell from 16,892 to 7,515 bytes (55.5%)
relative to commit `627e65e`, with detailed procedures retained in conditional
references. This is a byte count, not measured model context or latency savings.
