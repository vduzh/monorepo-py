import unittest

import dspy
from dspy import Module
from dspy.evaluate import answer_exact_match, answer_passage_match, Evaluate


class TestMetrics(unittest.TestCase):

    def test_simple_metric(self):
        def validate_answer(example, pred, trace=None):
            return example.answer.lower() == pred.answer.lower()

    def test_complex_metric(self):
        # Checks for multiple properties
        def validate_context_and_answer(example, pred, trace=None):
            # check the gold label and the predicted answer are the same
            answer_match = example.answer.lower() == pred.answer.lower()

            # check the predicted answer comes from one of the retrieved contexts
            context_match = any((pred.answer.lower() in c) for c in pred.context)

            if trace is None:  # if we're doing evaluation or optimization
                return (answer_match + context_match) / 2.0
            else:  # if we're doing bootstrapping, i.e. self-generating good demonstrations of each step
                return answer_match and context_match

    def test_built_in_answer_exact_match(self):
        answer_exact_match()
        pass

    def test_built_in_answer_passage_match(self):
        answer_passage_match()
        pass

    def test_simple_evaluation(self):
        # development set
        dev_set = [
            dspy.Example(question="What is the capital of Germany?", answer="Berlin").with_inputs("question"),
            dspy.Example(question="What is the capital of Great Britain?", answer="London").with_inputs("question"),
        ]

        # test program
        class TestProgram(Module):

            def forward(self, question):
                if "Germany" in question:
                    return dspy.Example(question=question, answer="Berlin")
                else:
                    return dspy.Example(question=question, answer="London")

        program = TestProgram()

        # simple metric
        def metric(example, pred, trace=None):
            return example.answer.lower() == pred.answer.lower()

        # evaluate
        scores = []
        for e in dev_set:
            pred = program(**e.inputs())
            score = metric(e, pred)
            scores.append(score)

        print("scores", scores)

    def test_evaluate(self):
        dev_set = [
            dspy.Example(question="What is the capital of Germany?", answer="Berlin").with_inputs("question"),
            dspy.Example(question="What is the capital of Great Britain?", answer="London").with_inputs("question"),
        ]

        # test program
        class TestProgram(Module):

            def forward(self, question):
                return dspy.Example(question="What is the capital of Germany?", answer="Berlin")

        program = TestProgram()

        # Set up the evaluator, which can be re-used in your code.
        evaluator = Evaluate(devset=dev_set, num_threads=1, display_progress=True, display_table=5)

        # Launch evaluation.
        res = evaluator(program, metric=answer_exact_match)
        print(res)

    def test_evaluate_with_ai(self):
        # Define the signature for automatic assessments.
        class Assess(dspy.Signature):
            """Assess the quality of a tweet along the specified dimension."""

            assessed_text = dspy.InputField()
            assessment_question = dspy.InputField()
            assessment_answer = dspy.OutputField(desc="Yes or No")

        gpt4_t = dspy.OpenAI(model='gpt-4-1106-preview', max_tokens=1000, model_type='chat')

        def metric(gold, pred, trace=None):
            question, answer, tweet = gold.question, gold.answer, pred.output

            engaging = "Does the assessed text make for a self-contained, engaging tweet?"
            correct = f"The text should answer `{question}` with `{answer}`. Does the assessed text contain this answer?"

            with dspy.context(lm=gpt4_t):
                correct = dspy.Predict(Assess)(assessed_text=tweet, assessment_question=correct)
                engaging = dspy.Predict(Assess)(assessed_text=tweet, assessment_question=engaging)

            correct, engaging = [m.assessment_answer.lower() == 'yes' for m in [correct, engaging]]
            score = (correct + engaging) if correct and (len(tweet) <= 280) else 0

            if trace is not None: return score >= 2
            return score / 2.0


if __name__ == '__main__':
    unittest.main()
