import unittest
from pprint import pprint

import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric
from dspy.teleprompt import BootstrapFewShotWithRandomSearch, BootstrapFewShot

from libs.dspy.constants import QUESTION, ANSWER
from libs.dspy.model import get_lm
from libs.dspy.simple_program import SimpleProgram


class TestOptimizers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lm = get_lm()
        dspy.settings.configure(lm=lm)

    def test_compile_program(self):
        # Load math questions from the GSM8K dataset
        gsm8k = GSM8K()
        # Create the train and dev sets
        gsm8k_train_set, gsm8k_dev_set = gsm8k.train[:10], gsm8k.dev[:10]

        # Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 4-shot examples of the program.
        config = dict(
            max_bootstrapped_demos=4,
            max_labeled_demos=4
        )
        # Optimize!
        # Use the `gsm8k_metric` here. In general, the metric is going to tell the optimizer how well it's doing.
        teleprompter = BootstrapFewShot(metric=gsm8k_metric, **config)

        # Compile (optimize) the DSPy program
        compiled_program = teleprompter.compile(
            SimpleProgram(),
            trainset=gsm8k_train_set
        )

        # Call the program with input argument
        result = compiled_program(question=QUESTION)
        print(result)

        # Inspect the last prompt for the LM
        print("\n\n=== Inspect the last prompt for the LM ===")
        dspy.settings.lm.inspect_history(n=1)

        # Assert the result
        self.assertEqual(2, len(result))
        self.assertEqual(ANSWER, result.answer)

    def test_bootstrap_few_shot(self):
        """If you have very little data, e.g. 10 examples of your task"""

        # the BootstrapFewShot is not an optimizing teleprompter

        pprint("Testing foo")
        self.assertTrue(True)

    def test_bootstrap_few_shot_with_random_search(self):
        """If you have slightly more data, e.g. 50 examples of your task"""

        # Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 8-shot examples of your program's steps.
        # The optimizer will repeat this 10 times (plus some initial attempts) before selecting its best attempt on the devset.
        config = dict(max_bootstrapped_demos=3, max_labeled_demos=3, num_candidate_programs=10, num_threads=4)

        teleprompter = BootstrapFewShotWithRandomSearch(metric=YOUR_METRIC_HERE, **config)
        optimized_program = teleprompter.compile(YOUR_PROGRAM_HERE, trainset=YOUR_TRAINSET_HERE)

        pprint("Testing foo")
        self.assertTrue(True)

        # Saving a program
        optimized_program.save(YOUR_SAVE_PATH)

        # Loading a program
        loaded_program = YOUR_PROGRAM_CLASS()
        loaded_program.load(path=YOUR_SAVE_PATH)

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


if __name__ == '__main__':
    unittest.main()
