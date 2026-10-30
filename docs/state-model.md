# Dialectical state model

Status: **draft for discussion.** This describes the intended model. The skills
do not fully implement it yet; section 7 lists the changes it implies.

## 1. Where the state lives

Each skill is stateless. The conversation is not: every turn, including every
operation, writes into the visible context, and the next turn reads that context
as its state. Dialectical has no other store in ChatGPT.

Two consequences follow:

- **State is only what the visible context supports.** Truncation,
  summarization, or a new thread loses it. Never reconstruct state that is no
  longer visible (the core skill already forbids inventing a history of
  suggestions or declines).
- **SAVE is serialization.** Exporting the state is the only way to carry it
  into another conversation.

The state has four parts:

| Part | What it holds | Written by |
|---|---|---|
| Claims | each consequential claim's status, origin, and basis | ordinary conversation and moves |
| Milestones | the latest distillation and its diff from the previous one | DISTILL |
| Plans | open proposals for evidence to collect, tests to run, signals to watch | planning operations |
| Interaction | pending menus, offers made or declined, stop-suggestion requests | onboarding and the core Monitor rule |

## 2. The conversation timeline

A conversation is a series of **segments** separated by **milestones**. Within a
segment, the user and the assistant move freely, in any order and as often as
they like. Most turns are ordinary conversation, not operations.

```text
new idea → discuss → explore → DISTILL ─┐
                                        │ milestone 1
explore → explore → DISTILL ────────────┤
                                        │ milestone 2: diff vs 1
CHALLENGE → acknowledge issues → DISTILL┘
                                          milestone 3: diff vs 2
```

**A distillation is a milestone, not a reset.**

- The transcript stays authoritative. A distillation is a dated snapshot of what
  the conversation supports at that point, and it can be wrong.
- Each distillation after the first states what changed since the previous one:
  which claims moved, on what evidence or analysis, and what was dropped. That
  diff is where status changes become visible and auditable.
- A later distillation can correct an earlier one. It says so rather than
  silently replacing it.

A reset design, in which later reasoning starts from the distillation and drops
the transcript, was rejected. It would turn any overstatement in a distillation
into the premise for everything after it.

Because most state changes happen in ordinary turns that nothing records, the
milestone is the only point where the claim state is made explicit. This is why
DISTILL is central.

## 3. Claim lifecycle

Statuses follow DISTILL, plus one proposed addition:

| Status | Meaning |
|---|---|
| Speculative | raised as a possibility with little support |
| Generated | hypothesized, inferred, or argued in the conversation; not checked against evidence |
| Tested | checked against identified evidence; survived a limited test |
| Established | the exact, limited observation directly supported by inspected evidence |
| **Refuted** (proposed) | contradicted by identified evidence or shown to fail by analysis |

A VERIFY verdict of *mixed* leaves the claim tested, with the conflict recorded.
A challenge the claim survives does not move it: it remains where it was, with
the challenge noted. An unsuccessful challenge does not verify anything.

**Legal transitions** need new evidence or explicit analysis, in either
direction:

- up: speculative → generated → tested → established;
- down: established → tested, or tested → generated, when new evidence narrows
  or undermines the basis;
- to refuted: from any status, on contradicting evidence or demonstrated failure;
- out of refuted: only on new evidence that removes the contradiction.

**Illegal transitions** are any change driven by pressure, repetition,
insistence, authority, flattery, coherence, the assistant's earlier agreement,
or independent workers reaching the same conclusion from the same inputs. This
is the hold-or-update principle in the core skill. The pressure study
(`QA/protocols/pressure-study.md`) measures how often illegal transitions occur.

**Origin is a separate dimension, not a status.** Whether a claim was
user-asserted, sourced, or model-generated (#28) is recorded alongside its
status. A model-generated claim can be tested; a sourced claim can be speculative.

## 4. Operation categories

Categories are defined by what each operation may read and write. That makes
them testable: an operation writing state outside its category is a defect.

| Category | Purpose | Reads | May write | Operations |
|---|---|---|---|---|
| **Moves** | think and test | conversation, claims | claim status, on evidence or analysis only | HYPOTHESIZE, THOUGHT EXPERIMENT, CHALLENGE, VERIFY, RESEARCH, ACH, CAUSAL-CHAIN, SOURCE-QUALITY |
| **Milestone** | mark where the thinking stands | conversation, previous milestone | a new snapshot and its diff | DISTILL |
| **Planning** | decide what to do outside the conversation | claims, latest milestone | plans only; never claim status | COLLECTION GAPS, TEST DESIGN, INDICATORS |
| **Metadata** | look at the conversation itself | history | nothing | TRACE, RECAP, RESTATE |
| **Logistics** | move state in or out of the conversation | latest milestone, claims, plans | an export, or imported context | SAVE, RESUME; file-store operations in non-ChatGPT editions |
| **Onboarding** | learn and choose operations | interaction state | interaction state only | GUIDE, HELP, JOIN, cookbook, flows |

**Planning** produces actions to take outside the conversation: evidence to
collect, tests to run, signals to watch. It is defined by its output, not its
timing. COLLECTION GAPS and TEST DESIGN are often most useful mid-inquiry, to
get unstuck between competing explanations. INDICATORS is usually used after a
conclusion or decision. None of them changes what is believed; they change what
the user will do next.

**Metadata** is read-only. RECAP and TRACE describe the conversation; they do
not add conclusions or move claims. RESTATE articulates a claim without
changing it.

**CHECKPOINT is removed.** A distillation is the checkpoint. In editions with a
file store, persisting a checkpoint is DISTILL followed by SAVE to a file.

## 5. Interaction state

Onboarding and the core Monitor rule keep a small amount of state, all of it
recoverable only from visible context.

| Machine | States | Transitions |
|---|---|---|
| GUIDE menu | idle → menu shown → catalog shown | At menu shown, a number or name runs only that operation, then returns to idle. MORE moves to catalog shown, which runs nothing and waits for a named command. Ignoring either returns to idle; nothing runs. |
| JOIN menu | idle → choices shown | RECAP, DISTILL, or TRACE runs once, with nothing chained after it; CONTINUE returns to ordinary conversation. After a decline, the menu returns only if the user invokes JOIN again; new context does not reactivate it. |
| Monitor offer (per claim) | not offered → offered → accepted or declined | Each claim is offered at most once. A decline holds until the claim changes materially or new evidence arrives; paraphrase does not reset it. |
| Stop suggestions (global) | on → off | Stays off until the user turns it back on. |

## 6. Rules the model implies

1. No operation changes a claim's status except a move or a milestone, and only
   on evidence or analysis.
2. Metadata and onboarding never change claims.
3. Planning output is a proposal; it is never evidence that the plan was carried out.
4. Every distillation after the first includes a diff from the previous one.
5. SAVE exports the latest milestone, open plans, claim origins, and open
   questions. It does not export interaction state.
6. A cold read (#27) exports the claims under test with every status set to
   generated, so the receiving chat evaluates them without inherited confidence.

## 7. Changes this implies

| Change | Where |
|---|---|
| DISTILL reports changes since the previous distillation, not only since the start | `dialectical-distill` |
| Add a refuted status and downward transitions | `dialectical-distill`, core skill |
| Record origin alongside status | #28 |
| Remove CHECKPOINT in every edition; DISTILL + SAVE replaces it where files exist | #29 (scope widens) |
| Group operations by these six categories in HELP and GUIDE | #30 |
| SAVE serializes per rule 5; cold read per rule 6 | `dialectical-save`, #27 |
| One negative QA case per category write rule (e.g. RECAP must not move a claim) | `QA/cases/` |

## 8. Open questions

- **Where does RELEVANCE belong?** It sets the inquiry's purpose and scope
  rather than planning future work or moving claims. Options: a seventh
  category (framing), or a move whose output is the frame rather than a claim.
- **Should START INQUIRY and CLOSE survive?** Under this model, the start is
  the first turn and the close is the final distillation plus an optional SAVE.
- **How explicit should status be in ordinary turns?** This model makes status
  visible at milestones only. Showing it continuously would make the
  conversation more formal, which the core skill avoids.
