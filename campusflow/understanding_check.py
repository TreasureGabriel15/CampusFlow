QUESTIONS = [
    {
        "prompt": "Ticket T001 is open and unassigned. A user tries to move it to in_progress.",
        "choices": [("A", "Accept"), ("B", "Reject and preserve all data"), ("C", "Resolve it automatically"), ("D", "Remove the ticket")],
        "answer": "B",
    },
    {
        "prompt": "The app has zero tickets. What should the resolution percentage display?",
        "choices": [("A", "Crash"), ("B", "100%"), ("C", "0%"), ("D", "Divide by one")],
        "answer": "C",
    },
    {
        "prompt": "Filter title 'wifi', category Network, status open. Which records should match?",
        "choices": [("A", "Any record matching one filter"), ("B", "Only records matching all supplied filters"), ("C", "All network records"), ("D", "All open records")],
        "answer": "B",
    },
    {
        "prompt": "A resolved ticket receives Add note. What should happen?",
        "choices": [("A", "Append anyway"), ("B", "Delete old notes"), ("C", "Reject until reopened"), ("D", "Change status silently")],
        "answer": "C",
    },
    {
        "prompt": "The JSON file includes two tickets with the same ID. What should load do?",
        "choices": [("A", "Keep both"), ("B", "Replace memory with the duplicates"), ("C", "Reject the load without changing current memory"), ("D", "Rename the IDs silently")],
        "answer": "C",
    },
    {
        "prompt": "A pull request changes validation but has no negative-case tests. Best review action?",
        "choices": [("A", "Approve because it runs"), ("B", "Request focused tests and reasoning"), ("C", "Merge immediately"), ("D", "Ask AI to approve it")],
        "answer": "B",
    },
]

def score_answers(answers):
    if len(answers) != len(QUESTIONS):
        raise ValueError("The quiz needs one answer for each question.")
    score = 0
    for answer, question in zip(answers, QUESTIONS):
        if str(answer).strip().upper() == question["answer"]:
            score += 1
    return score