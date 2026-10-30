# Portable conversation handoff

The handoff must be useful when it is the only context supplied to a fresh
thread. Prefer compact prose and omit empty sections, but retain these meanings:

- **Title and purpose:** what the inquiry is about and what the conversation is
  trying to understand, decide, or explore.
- **Essential context:** terms, actors, scope, time horizon, and constraints that
  would otherwise be unclear.
- **Current state:** conclusions, decisions, and material developments, each at
  the confidence actually earned.
- **Evidence and provenance:** what supports the current state, where it came
  from, and any source or verification limits. Label the origin of each
  consequential claim: user-supplied, sourced (name the source), or
  assistant-generated without a source. Keep any flag that an
  assistant-generated claim is being used as a premise; the receiving thread
  must not treat it as sourced.
- **Live alternatives:** hypotheses, disagreements, or abandoned paths that
  still matter, including why they remain open or were set aside.
- **Uncertainties and gaps:** unknowns, missing context, and unresolved conflicts.
- **Open questions and next moves:** the most useful ways to continue, presented
  as options rather than an automatic workflow.

End with a short continuation note telling the receiving thread to treat the
handoff as context rather than verified truth, preserve its qualifications, and
continue from the user's next request. Include useful source links or identifiers
when present. Do not include the full transcript unless the user explicitly asks.
