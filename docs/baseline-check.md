# Baseline Check

**Documentation owner (Engineer A):** Gabriel Odeh

## What CampusFlow must do

- Create tickets with a title, category, urgency, and positive whole-number user count.
- Calculate priority from urgency and the number of affected users.
- Assign staff and move tickets through `open` → `in_progress` → `resolved`; reopening returns a resolved ticket to `open`.
- Add notes to tickets that are not resolved. Notes need an author and a 5–300 character message.
- Save and load tickets while rejecting malformed records, invalid or duplicate IDs, and inconsistent ticket data.

## Baseline result

Run the test suite with:

```sh
python3 -m unittest discover -s tests -v
```

**Checked:** 101 tests passed.

The tests cover ticket creation and priority, workflow transitions, notes, and saving/loading data, including invalid-input cases.
