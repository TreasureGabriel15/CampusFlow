# CampusFlow

CampusFlow is a text-based campus help desk for recording and managing reports about problems such as broken Wi-Fi, laptops, and software. It stores reports as tickets, calculates their priority, tracks assignment and status, and saves the data locally as JSON.

## What it does

- Create tickets with a title, category, urgency, and number of affected users.
- Calculate ticket priority automatically:

  | Condition | Priority |
  |---|---|
  | High urgency and at least 10 affected users | Critical |
  | High urgency or at least 10 affected users | High |
  | Medium urgency or at least 3 affected users | Medium |
  | Any other valid combination | Low |

- Assign staff to tickets and track their progress.
- Show an unresolved work queue, ordered by priority.
- Search tickets by title, category, status, and priority.
- View ticket summaries by status, priority, and category.
- Add and view updates (notes) on tickets. A note needs an author and a message of 5–300 characters. Resolved tickets cannot receive notes unless reopened.
- Take a short understanding-check quiz.
- Save and reload tickets in `tickets.json`. Invalid or duplicate ticket data is rejected instead of silently loaded.

## Requirements

- Python 3.8 or newer.
- No third-party Python packages are required; the application and tests use the Python standard library.

## Run the application

1. Open a terminal in the project directory (the directory containing `main.py`).
2. Start CampusFlow:

   ```sh
   python3 main.py
   ```

   On Windows, use `python main.py` if that is how Python is installed on your system.

3. Choose an action from the menu:

   | Choice | Action | What to enter |
   |---|---|---|
   | 1 | Queue | Displays unresolved tickets in priority order. |
   | 2 | Create | Enter a title, category (`Network`, `Hardware`, `Software`, or `Other`), urgency (`low`, `medium`, or `high`), and positive whole number of affected users. |
   | 3 | Assign | Enter the ticket ID and a staff member's name. |
   | 4 | Status | Enter the ticket ID and its next status. Tickets move from `open` to `in_progress` to `resolved`; assign a staff member before moving a ticket to `in_progress`. |
   | 5 | Reopen | Enter a resolved ticket's ID to return it to `open`. |
   | 6 | Report | Shows ticket totals and breakdowns by status, priority, and category. |
   | 7 | Search | Enter any combination of title text, category, status, and priority. Leave a filter blank to match any value. |
   | 8 | Add note | Enter a ticket ID, author, and update message. |
   | 9 | View notes | Enter a ticket ID to display its saved updates. |
   | 10 | Quiz | Answer the six multiple-choice questions, then enter two short explanations. |
   | 11 | Exit | Saves ticket data and closes the program. |

4. When a ticket is created or changed, CampusFlow saves the data to `tickets.json` in the current project directory. The file is created automatically if it does not already exist. Keep it between runs to retain your tickets.

## Run the tests

From the project directory, run the full test suite using Python's built-in `unittest`:

```sh
python3 -m unittest discover -s tests -v
```

The tests cover ticket validation and priority, workflow transitions, search, reports, notes, and data persistence.

## Project layout

```text
main.py                    Command-line application
campusflow/                Ticket, workflow, storage, report, search, and quiz logic
tests/                     Automated tests
docs/                      Learning log, baseline check, and design decisions
tickets.json               Local ticket data, created when the application saves
```
