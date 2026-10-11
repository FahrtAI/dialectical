# ACH worked example

The evidence here is illustrative.

## Observation

Last quarter, enterprise prospects who attended at least one webinar converted at three times the rate of those who did not (about 2,000 prospects). Question: what is the main source of the gap?

## Hypotheses

- **H1 Persuasion** (offered): the webinars themselves move prospects toward buying.
- **H2 Selection** (added): prospects already close to buying are the ones who attend. This also covers the measurement-artifact reading, that attendance signals buying mode.
- **H3 Follow-up** (added): sales gives attendees more attention afterward.
- **H4 Comparison pool** (added): the non-attendee group includes many leads who were never invited.
- **H5 Chance** (added): sampling variation accounts for a material part of the observed gap.

Skipped from the checklist: concurrent events (both groups saw the same quarter),
regression to the mean (no group was chosen for an extreme starting value), and
reverse causation (conversion cannot precede attendance; buying intent driving
attendance is H2). Chance is retained because total sample size and a relative
gap are not enough to assess it without group sizes, conversion counts, or an
appropriate uncertainty estimate.

## Evidence

| | Evidence | H1 | H2 | H3 | H4 | H5 |
|---|---|---|---|---|---|---|
| E1 | Before the webinar, attendees had 2.5× the demo requests of non-attendees (CRM) | - | ++ | 0 | + | ? |
| E2 | Attendees received about twice the follow-up touches in the next 30 days (activity logs) | 0 | 0 | + | 0 | ? |
| E3 | Among prospects matched on pre-webinar engagement, the gap falls to 1.3× (CRM) | -- | ++ | - | + | ? |
| E4 | About 40% of non-attendees were never on an invitation list | 0 | 0 | 0 | + | ? |
| E5 | Attendees rate the webinars 4.6/5 | + | + | + | + | ? |
| E6 | Among invited prospects only, the gap is still 2.8× | + | + | + | -- | ? |

## Notes

- **Diagnosticity:** E5 fits every hypothesis, so it does not help choose. E3 and E6 are the most diagnostic items.
- **Source dependence:** E1 and E3 both come from CRM engagement records. If that tracking is incomplete, both weaken together; they are not independent support.
- **Overlap:** the causes can combine. The question is which accounts for most of the gap, not which is the only cause.

## Assessment

H2 (selection) is the least inconsistent of the mechanism explanations. H1 as
the main source faces a strong contradiction in E3: once prior engagement is
matched, most of the gap disappears. H4 faces one in E6: removing uninvited
leads barely changes the gap. E2 shows that attendees received more follow-up,
but not that follow-up caused conversion, so H3 may contribute but remains
untested as a causal explanation. H5 cannot be assessed from the supplied
aggregates; its all-`?` row is unresolved, not evidence that chance is likely.

## Sensitivity and residual uncertainty

- H2's lead rests mainly on E1 and E3, which share a source. If the CRM undercounts engagement, the matching in E3 is weaker than it looks and H1 recovers.
- The H3 rating on E3 assumes matched attendees still received more follow-up. That has not been checked.
- The remaining 1.3× is unexplained; persuasion, follow-up, or both could account for it.
- The missing group sizes and conversion counts prevent an assessment of how
  much sampling variation could explain.

## Next test

Audit CRM engagement coverage for a sample of prospects. It is cheap, and it tests the evidence the result depends on most. If coverage holds, split the remaining 1.3× by also matching on follow-up touches, which separates H1 from H3.
