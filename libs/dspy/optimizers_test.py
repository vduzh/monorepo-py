import os.path
import unittest
from pprint import pprint

import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric
from dspy.teleprompt import BootstrapFewShotWithRandomSearch, BootstrapFewShot

from libs.dspy.utils.constants import MATH_QUESTION, MATH_ANSWER
from libs.dspy.utils.model import get_lm
from libs.dspy.utils.simple_program import SimpleProgram


class TestOptimizers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lm = get_lm()
        dspy.settings.configure(lm=lm)

        # Load math questions from the GSM8K dataset
        cls.gsm8k = GSM8K()

    def test_labeled_few_shot(self):
        pass

    def test_bootstrap_few_shot(self):
        """ If you have very little data, e.g. 10 examples of your task."""

        # Specify the metric to use
        metric = gsm8k_metric

        # Create the optimizer configuration
        config = dict(
            # bootstraps 4-shot examples of the program
            max_bootstrapped_demos=4,
            # the number of demonstrations randomly selected from the trainset
            max_labeled_demos=4
        )

        #  Instantiate an optimizer with the metric and config
        optimizer = BootstrapFewShot(metric=metric, **config)

        # Optimize the program
        # train_set = self.gsm8k.train[:10]
        # optimized_program = optimizer.compile(SimpleProgram(), trainset=train_set)

    def test_bootstrap_few_shot_with_random_search(self):
        """If you have slightly more data, e.g. 50 examples of your task"""

        # Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 8-shot examples of your program's steps.
        # The optimizer will repeat this 10 times (plus some initial attempts) before selecting its best attempt on
        # the dev set.
        config = dict(
            max_bootstrapped_demos=4,
            max_labeled_demos=4,
            num_candidate_programs=10,
            num_threads=4
        )

        # Instantiate an object from the class
        optimizer = BootstrapFewShotWithRandomSearch(metric=gsm8k_metric, **config)

        # Optimize the program
        train_set = self.gsm8k.train[:50]
        optimized_program = optimizer.compile(SimpleProgram(), trainset=train_set)

        # result = optimized_program(question=MATH_QUESTION)
        # print("Result:", result)

    def test_mipro(self):
        """If you have more data than that, e.g. 300 examples or more"""
        pprint("Testing foo")
        self.assertTrue(True)

    def test_bootstrap_finetune(self):
        """
        If you have been able to use one of these with a large LM (e.g., 7B parameters or above) and need
        a very efficient program, compile that down to a small LM
        """
        pprint("Testing foo")
        self.assertTrue(True)

    def test_compile_and_save_program(self):
        """Optimize the program and save the results to the file"""

        # 1. Create a train sets from the gsm8k data set
        train_set = self.gsm8k.train[:10]

        # 2. Set up the optimizer
        optimizer = BootstrapFewShot(metric=gsm8k_metric, max_bootstrapped_demos=4, max_labeled_demos=4)

        # 3. Compile (optimize) the DSPy program
        optimized_program = optimizer.compile(SimpleProgram(), trainset=train_set)

        # 4. Save the program to the file
        optimized_program.save(os.path.relpath("tmp/optimized_simple_program.json"))

    def test_load_optimized_program(self):
        """Load the program from the file and used for inference"""

        # 1. Instantiate an object from the class
        program = SimpleProgram()

        # 2. Call the load method on the object
        program.load(path=os.path.relpath("data/optimized_simple_program.json"))

        # 3. Call the program with input argument for inference.
        result = program(question=MATH_QUESTION)

        # Inspect the last prompt for the LM
        dspy.settings.lm.inspect_history(n=1)
        # Print the result
        print("Result:", result)

        # Assert the result
        self.assertEqual(2, len(result))
        self.assertEqual(MATH_ANSWER, result.answer)


if __name__ == '__main__':
    unittest.main()
