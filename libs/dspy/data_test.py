import unittest

import dspy
from dspy import Example
from dspy.datasets import HotPotQA
from dspy.datasets.gsm8k import GSM8K


def print_example(title: str, example: Example):
    # use list comprehension to initialize a dictionary
    # data = {key: example.get(key) for key in example.keys()}

    # print(title, json.dumps(data, indent=2))
    # print(title, data)
    print(title, example)


class TestData(unittest.TestCase):

    def test_example(self):
        example = dspy.Example(foo="Foo", bar="Bar")
        print(example)

        self.assertEqual("Foo", example.foo)
        self.assertEqual("Bar", example.bar)

    def test_example_with_inputs(self):
        qa_example = dspy.Example(question="This is a question?", answer="This is an answer.")

        # Single Input
        s_input_example = qa_example.with_inputs("question")
        print(s_input_example)

        # Multiple Input
        m_input_example = qa_example.with_inputs("question", "answer")
        print(m_input_example)

        # Inputs
        input_keys_example = s_input_example.inputs()
        print(input_keys_example)
        self.assertIsNotNone(input_keys_example.question)
        self.assertIsNone(input_keys_example.get("answer"))

        # Labels
        label_keys_example = s_input_example.labels()
        print(label_keys_example)
        self.assertIsNotNone(label_keys_example.answer)
        self.assertIsNone(label_keys_example.get("question"))

    def test_training_set(self):
        train_set = [
            dspy.Example(report="Long report 1", summary="Short summary 1"),
            dspy.Example(report="Long report 2", summary="Short summary 2"),
        ]
        print(train_set)

    def test_data_set(self):
        raise NotImplementedError()

    def test_hot_pot_qa_data_set(self):
        # Load the dataset with data and addition labels from Wikipedia
        data_set = HotPotQA(
            train_seed=1,
            train_size=20,
            eval_seed=2023,
            dev_size=50,
            test_size=5,
        )

        print_example("data_set::train:example", data_set.train[0])
        print_example("data_set::dev:example", data_set.dev[0])
        print_example("data_set::test:example", data_set.test[0])

        # Tell DSPy that the 'question' field is the input. Any other fields are labels and/or metadata.
        train_set = [x.with_inputs('question') for x in data_set.train]
        dev_set = [x.with_inputs('question') for x in data_set.dev]
        test_set = [x.with_inputs('question') for x in data_set.test]

        train_example = train_set[0]
        print_example("Train example:", train_example)

        dev_example = dev_set[0]
        print_example("Dev example:", dev_example)

        test_example = test_set[0]
        print_example("Test example:", test_example)

    def test_gsm8k_data_set(self):
        # Load math questions from the GSM8K dataset
        data_set = GSM8K()

        print_example("data_set::train:example", data_set.train[0])
        print_example("data_set::dev:example", data_set.dev[0])

        # # Tell DSPy that the 'question' field is the input. Any other fields are labels and/or metadata.
        train_set = [x.with_inputs('question') for x in data_set.train]
        dev_set = [x.with_inputs('question') for x in data_set.dev]

        train_example = train_set[0]
        print_example("Train example:", train_example)

        dev_example = dev_set[0]
        print_example("Dev example:", dev_example)


if __name__ == '__main__':
    unittest.main()
