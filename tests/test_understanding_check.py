import unittest

from campusflow.understanding_check import QUESTIONS, score_answers


class TestQuestionsData(unittest.TestCase):
    def test_there_are_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_every_question_has_required_keys(self):
        for question in QUESTIONS:
            self.assertEqual(set(question), {"prompt", "choices", "answer"})

    def test_every_question_has_four_choices_a_to_d(self):
        for question in QUESTIONS:
            letters = [letter for letter, _ in question["choices"]]
            self.assertEqual(letters, ["A", "B", "C", "D"])

    def test_every_answer_is_one_of_the_choices(self):
        for question in QUESTIONS:
            letters = {letter for letter, _ in question["choices"]}
            self.assertIn(question["answer"], letters)

    def test_prompts_are_not_empty(self):
        for question in QUESTIONS:
            self.assertTrue(question["prompt"].strip())


class TestScoreAnswers(unittest.TestCase):
    def setUp(self):
        self.correct = [q["answer"] for q in QUESTIONS]

    def test_all_correct(self):
        self.assertEqual(score_answers(self.correct), len(QUESTIONS))

    def test_none_correct(self):
        wrong = ["A" if a != "A" else "B" for a in self.correct]
        self.assertEqual(score_answers(wrong), 0)

    def test_partial_score(self):
        answers = list(self.correct)
        answers[0] = "A" if answers[0] != "A" else "B"
        answers[1] = "A" if answers[1] != "A" else "B"
        self.assertEqual(score_answers(answers), len(QUESTIONS) - 2)

    def test_lowercase_answers_are_accepted(self):
        self.assertEqual(score_answers([a.lower() for a in self.correct]), len(QUESTIONS))

    def test_whitespace_is_ignored(self):
        self.assertEqual(score_answers([f"  {a} " for a in self.correct]), len(QUESTIONS))

    def test_too_few_answers_raises(self):
        with self.assertRaises(ValueError):
            score_answers(self.correct[:-1])

    def test_too_many_answers_raises(self):
        with self.assertRaises(ValueError):
            score_answers(self.correct + ["A"])

    def test_empty_list_raises(self):
        with self.assertRaises(ValueError):
            score_answers([])

    def test_error_message_is_helpful(self):
        with self.assertRaises(ValueError) as ctx:
            score_answers(["A"])
        self.assertIn("one answer for each question", str(ctx.exception))

    def test_invalid_letter_scores_zero_not_crash(self):
        self.assertEqual(score_answers(["Z"] * len(QUESTIONS)), 0)

    def test_non_string_answers_do_not_crash(self):
        self.assertEqual(score_answers([None] * len(QUESTIONS)), 0)

    def test_does_not_modify_input(self):
        answers = list(self.correct)
        score_answers(answers)
        self.assertEqual(answers, self.correct)


if __name__ == "__main__":
    unittest.main()