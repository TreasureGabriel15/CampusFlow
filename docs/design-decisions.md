# Design Decisions

**Engineer A:** Gabriel Odeh

| Decision | Reason |
|---|---|
| Store tickets as JSON. | It is a simple format for this text-only application and keeps saved data readable. |
| Use Python's built-in `unittest`. | The suite can run without installing a test framework. |
| Normalize user-provided status values and restrict valid transitions. | This accepts common input variations without allowing tickets to skip workflow stages. |
| Calculate priority from urgency and affected-user count. | The rules are consistent and covered by tests. High urgency affecting at least 10 people is critical; high urgency or at least 10 people is high; medium urgency or at least 3 people is medium; otherwise it is low. |
| Validate tickets and notes when loading saved data. | Invalid records, duplicate IDs, and inconsistent priority should not enter the application. |
| Keep note IDs sequential within each ticket and prevent notes on resolved tickets. | Updates stay associated with their ticket, and resolved tickets remain locked until reopened. |
**Engineer B:** Treasure Gabriel

| Decision | Reason |
| --- | --- |
| Search titles with `casefold()` and a substring check. | `Wi-Fi` and `wi-fi` match. The search does not correct spelling, and it does not change any ticket. |
| Combine category, status, and priority with AND. | A blank filter is ignored. Every filter the user fills in must match. |
| Keep the Open Work Queue limited to status `open`. | `in_progress` and `resolved` tickets stay out of that queue. Same priority uses the numeric ID, so `T2` comes before `T10`. |
| Count unresolved as `open` plus `in_progress`, and show 0% when there are no tickets. | A reopened ticket is counted by its current status. An empty list must not divide by zero. |
| Keep quiz questions separate from `score_answers`. | The menu can reject a bad letter and ask again. The score still uses the answers that were actually saved. Explanations are not auto-graded. |
| Call `add_note` from the menu, but do not enforce note rules there. | Author, message length, and the resolved-ticket lock belong to Engineer A's notes code. A rejected note must not be saved. |
