# AI Learning Log

**Documentation owner (Engineer A):** Gabriel Odeh

This is a concise summary of the team's recorded AI-assisted work. Contributor credits are unchanged.

| Topic | AI suggestion | Team decision | Recorded contributor |
|---|---|---|---|
| Workflow input | Use a lookup table for valid status transitions. | Keep the transition table and normalize status input so spacing, case, and hyphens are handled consistently. | Treasure Gabriel |
| Tests | Use `pytest`. | Use Python's built-in `unittest` so tests can run in the available offline environment. | Treasure Gabriel |
| Ticket IDs | Start from a basic ticket-ID tracker. | Generate the next ID from the largest existing numeric ID, and test the empty-list case. | Serah John |

The implementation and test details are recorded in the project source and test suite.
