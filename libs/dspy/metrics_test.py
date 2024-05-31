import unittest

import dspy
from dsp import Example
from dspy.evaluate import answer_exact_match, answer_passage_match

from libs.dspy.utils.constants import ANSWER, QUESTION


class TestMetrics(unittest.TestCase):

    def test_built_in_answer_exact_match(self):
        example = Example(question=QUESTION, answer=ANSWER)
        pred = Example(question=QUESTION, answer=ANSWER)
        res = answer_exact_match(example, pred)

        self.assertTrue(res)

    def test_built_in_answer_passage_match(self):
        # TODO: not implemented
        example = Example(question=QUESTION, answer=ANSWER)
        pred = Example(question=QUESTION, answer=ANSWER)
        res = answer_passage_match(example, pred)

        self.assertTrue(res)

    def test_custom_simple_metric(self):
        # Create a metric function that returns either a number or a boolean value
        def validate_answer(example, pred, trace=None):
            return example.answer.lower() == pred.answer.lower()

    def test_custom_complex_metric(self):
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

    def test_custom_simple_ai_based_metric(self):
        class FactJudge(dspy.Signature):
            """Judge if the answer is factually correct based on the context."""

            context = dspy.InputField(desc="Context for the prediction")
            question = dspy.InputField(desc="Question to be answered")
            answer = dspy.InputField(desc="Answer for the question")

            factually_correct = dspy.OutputField(
                desc="Is the answer factually correct based on the context?",
                prefix="Factual[Yes/No]:"
            )

        def metric(example, pred):
            """ Asks LLM if the answer is factually correct based on the context."""

            # Use the ChainOfThought module to call LLM
            judge = dspy.ChainOfThought(FactJudge)

            # Call LLM to judge
            factual = judge(context=example.context, question=example.question, answer=pred.answer)
            return int(factual == "Yes")

    def test_custom_ai_based_metric(self):
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

            if trace is not None:
                return score >= 2

            return score / 2.0


if __name__ == '__main__':
    unittest.main()
