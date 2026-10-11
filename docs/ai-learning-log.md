# AI-Native Learning Log — Team: Treasure Gabriel & Serah John

### Interaction 1: Input Cleaning for Workflows (Treasure Gabriel)
* **AI Concept Suggested:** The AI suggested using a simple look-up dictionary (`_NEXT`) to map out how states progress one-way.
* **My Implementation/Correction:** I modified the logic by adding a heavy string sanitization process (`_status`) using a chain of `.strip().lower().replace()`. This ensures that even if users type messy statuses with spaces or hyphens, the workflow module cleans it up and processes it without crashing.

### Interaction 2: Transitioning from Pytest to Native Unittest (Treasure Gabriel)
* **AI Concept Suggested:** The AI model originally provided automated test files written for `pytest`.
* **My Implementation/Correction:** Our local laptop environment lacked `pytest` and `pip` installation access while working under a strict deadline. I independently converted the automated testing logic into Python's native `unittest` framework for `storage.py` and `workflow.py`, ensuring our test suite runs completely offline using `python3 -m unittest`.

### Interaction 3: Ticket ID Generation Optimization (Serah John)
* **AI Concept Suggested:** The AI model provided a basic string tracker template for parsing existing ticket tracking records inside `tickets.py`.
* **Serah's Correction:** Serah took the logic and optimized it inside `next_ticket_id` to cleanly parse digits by slicing strings (`int(t["id"][1:])`) and formatting the counter to dynamically generate incremental pad layouts (`f"T{max(numbers) + 1:03d}"`). She then updated `test_tickets.py` to assert edge cases for empty data arrays.
