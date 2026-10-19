# AI Learning Log

**Engineer A:** Gabriel Odeh

This is a concise summary of the team's recorded AI-assisted work. Contributor credits are unchanged.

| Topic | AI suggestion | Team decision | Recorded contributor |
|---|---|---|---|
| Workflow input | Use a lookup table for valid status transitions. | Keep the transition table and normalize status input so spacing, case, and hyphens are handled consistently. | Treasure Gabriel |
| Tests | Use `pytest`. | Use Python's built-in `unittest` so tests can run in the available offline environment. | Treasure Gabriel |
| Ticket IDs | Start from a basic ticket-ID tracker. | Generate the next ID from the largest existing numeric ID, and test the empty-list case. | Serah John |

The implementation and test details are recorded in the project source and test suite.


**Engineer B:** Treasure Gabriel

| Topic | What I asked | AI suggestion | What I decided |
| --- | --- | --- | --- |
| Search matching | How should a title search ignore capital letters without fuzzy spelling changes? | Use `str.lower()` for a simple case-insensitive contains check. | Use `casefold()` instead. It still does a substring match, so `WI-FI` matches `wi-fi`, but it does not turn `wifi` into `wi-fi`. Search returns a new list and does not edit the tickets. |
| Work queue | Should the original queue include `in_progress` tickets because they are unresolved? | Keep every ticket that is not `resolved`, then sort by priority and ID. | Reject that. The original Open Work Queue shows only status `open`. `in_progress` still counts as unresolved in the report, but it does not appear in that queue. Ties use the number inside the ID, not the text `T10` before `T2`. |

The implementation and test details are recorded in the project source and test suite.
