import unittest
from pprint import pprint

from dspy.teleprompt import BootstrapFewShotWithRandomSearch


class TestOptimizers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._foo = "foo"

    @classmethod
    def tearDownClass(cls):
        cls._foo = None

    def setUp(self):
        self._bar = "bar"

    def tearDown(self):
        self._bar = None

    def test_bootstrap_few_shot(self):
        """If you have very little data, e.g. 10 examples of your task"""
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
