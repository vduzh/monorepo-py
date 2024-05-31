import unittest

import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric
from dspy.evaluate import Evaluate, answer_exact_match
from dspy.teleprompt import BootstrapFewShot

from libs.dspy.utils.model import get_lm
from libs.dspy.utils.simple_program import SimpleProgram


class TestEvaluate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configure dspy
        dspy.settings.configure(lm=get_lm())

        # Load math questions from the GSM8K dataset
        gsm8k = GSM8K()
        cls.gsm8k_train_set, cls.gsm8k_dev_set = gsm8k.train[:10], gsm8k.dev[:10]

    def test_custom_evaluation(self):
        # Compose a development set
        dev_set = [
            dspy.Example(question="What is the capital of Germany?", answer="Berlin").with_inputs("question"),
            dspy.Example(question="What is the capital of Great Britain?", answer="London").with_inputs("question"),
        ]

        # Create a program instance
        program = SimpleProgram()

        # Evaluate
        scores = []
        for example in dev_set:
            pred = program(**example.inputs())
            score = answer_exact_match(example, pred)
            scores.append(score)

        print("Custom evaluation scores:", scores)

    def test_evaluate_program(self):
        # Create a program
        program = SimpleProgram()

        # Set up the evaluator, which can be used multiple times.
        evaluate = Evaluate(
            devset=self.gsm8k_dev_set,
            metric=gsm8k_metric,
            num_threads=4,
            display_progress=True,
            display_table=0
        )

        # Evaluate the `program`
        evaluate(program)

    def test_evaluate_compiled_program(self):
        # Create a program
        program = SimpleProgram()

        # Define the teleprompter and compile the program
        teleprompter = BootstrapFewShot(
            metric=gsm8k_metric,
            max_bootstrapped_demos=4,
            max_labeled_demos=4)
        compiled_program = teleprompter.compile(program, trainset=self.gsm8k_train_set)

        # Set up the evaluator, which can be used multiple times.
        evaluate = Evaluate(
            devset=self.gsm8k_dev_set,
            metric=gsm8k_metric,
            num_threads=4,
            display_progress=True,
            display_table=0
        )

        # Evaluate our `compiled_program`
        evaluate(compiled_program)


if __name__ == '__main__':
    unittest.main()
