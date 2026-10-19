# Design Decisions

**Documentation owner (Engineer A):** Gabriel Odeh

| Decision | Reason |
|---|---|
| Store tickets as JSON. | It is a simple format for this text-only application and keeps saved data readable. |
| Use Python's built-in `unittest`. | The suite can run without installing a test framework. |
| Normalize user-provided status values and restrict valid transitions. | This accepts common input variations without allowing tickets to skip workflow stages. |
| Calculate priority from urgency and affected-user count. | The rules are consistent and covered by tests. High urgency affecting at least 10 people is critical; high urgency or at least 10 people is high; medium urgency or at least 3 people is medium; otherwise it is low. |
| Validate tickets and notes when loading saved data. | Invalid records, duplicate IDs, and inconsistent priority should not enter the application. |
| Keep note IDs sequential within each ticket and prevent notes on resolved tickets. | Updates stay associated with their ticket, and resolved tickets remain locked until reopened. |
