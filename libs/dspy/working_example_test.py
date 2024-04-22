import unittest
from pprint import pprint
from unittest import TestCase

import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric
from dspy.evaluate import Evaluate
from dspy.teleprompt import BootstrapFewShot

from model import get_lm


class TestWorkingExample(TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the LM
        lm = get_lm()
        lm.inspect_history(n=1)
        dspy.settings.configure(lm=lm)

        # Load math questions from the GSM8K dataset
        gsm8k = GSM8K()
        cls.gsm8k_train_set, cls.gsm8k_dev_set = gsm8k.train[:10], gsm8k.dev[:10]

    def test_fake(self):
        print(self.gsm8k_train_set[:1])
        # pprint(self.gsm8k_dev_set[:1])

    def test_minimal_working_example(self):
        # Define the Module
        class CoT(dspy.Module):
            def __init__(self):
                super().__init__()
                self.prog = dspy.ChainOfThought("question -> answer")

            def forward(self, question):
                return self.prog(question=question)

        # Compile and Evaluate the Model

        # Set up the optimizer:
        # We want to "bootstrap" (i.e., self-generate) 4-shot examples of our CustomModule program.
        config = dict(max_bootstrapped_demos=4, max_labeled_demos=4)

        # Optimize! Use the `gsm8k_metric` here.
        # In general, the metric is going to tell the optimizer how well it's doing.
        teleprompter = BootstrapFewShot(metric=gsm8k_metric, **config)
        optimized_cot = teleprompter.compile(
            CoT(),
            trainset=self.gsm8k_train_set,
            valset=self.gsm8k_dev_set
        )

        # Evaluate

        # Set up the evaluator, which can be used multiple times.
        evaluate = Evaluate(
            devset=self.gsm8k_dev_set,
            metric=gsm8k_metric,
            num_threads=4,
            display_progress=True,
            display_table=0
        )

        # Evaluate our `optimized_cot` program.
        evaluate(optimized_cot)

        # run the program
        prediction = optimized_cot(question='What is the capital of Germany?')
        print(prediction)

        # assert the result
        self.assertEqual("Berlin", prediction.answer)


if __name__ == '__main__':
    unittest.main()
