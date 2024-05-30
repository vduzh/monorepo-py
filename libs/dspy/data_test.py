import unittest
from pprint import pprint

import dspy
import pandas as pd
from dspy import Example
from dspy.datasets import HotPotQA, DataLoader
from dspy.datasets.colors import Colors
from dspy.datasets.dataset import Dataset
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

        for k, v in example.items():
            print(f"{k} = {v}")

        self.assertEqual("Foo", example.foo)
        self.assertEqual("Bar", example.bar)

    def test_example_with_inputs(self):
        """with_inputs marks specific fields as inputs"""

        # test data
        example = dspy.Example(question="This is a question?", answer="This is an answer.")
        print("DataSet Entry:", example)

        # Single Input
        single_input_example = example.with_inputs("question")
        print("Single Input:", single_input_example)

        # Multiple Input
        multiple_input_example = example.with_inputs("question", "answer")
        print("Multiple Input:", multiple_input_example)

    def test_example_inputs_and_labels(self):
        # Init test data
        example = dspy.Example(
            context="This some context",
            question="This is a question?",
            answer="This is an answer."
        )

        # Build an example with the inputs specified
        input_example = example.with_inputs("context", "question")
        print("Example with inputs:", input_example)

        # Creates an examples with only 2 inputs specified above
        input_keys_example = input_example.inputs()
        print("Only inputs:", input_keys_example)

        self.assertIsNotNone(input_keys_example.context)
        self.assertIsNotNone(input_keys_example.question)
        self.assertIsNone(input_keys_example.get("answer"))

        # Creates an examples with one inputs specified above
        label_keys_example = input_example.labels()
        print("Only labels:", label_keys_example)

        self.assertIsNone(label_keys_example.get("context"))
        self.assertIsNone(label_keys_example.get("question"))
        self.assertIsNotNone(label_keys_example.answer)

    def test_data_set(self):
        # Dataset is just a list of Example objects
        train_set = [
            dspy.Example(report="Long report 1", summary="Short summary 1"),
            dspy.Example(report="Long report 2", summary="Short summary 2"),
        ]
        print(train_set)

    def test_built_in_hot_pot_qa_data_set(self):
        """HotPotQA is a collection of question-answer pairs"""

        # Load the dataset with data and addition labels from Wikipedia
        data_set = HotPotQA(
            train_seed=1,
            train_size=20,
            eval_seed=2023,
            dev_size=50,
            test_size=5,
        )

        train_set, dev_set, test_set = data_set.train, data_set.dev, data_set.test
        print_example("Train set example:", train_set[0])
        print_example("Dev set example:", dev_set[0])
        print_example("Test set example:", test_set[0])

    def test_built_in_gsm8k_data_set(self):
        # Load math questions from the GSM8K dataset
        data_set = GSM8K()

        train_set, dev_set, test_set = data_set.train, data_set.dev, data_set.test
        print_example("Train set example:", train_set[0])
        print_example("Dev set example:", dev_set[0])
        print_example("Test set example:", test_set[0])

    def test_built_in_color_data_set(self):
        # Load  questions from the Colors dataset
        data_set = Colors()

        train_set, dev_set = data_set.train, data_set.dev
        print_example("Train set example:", train_set[0])
        print_example("Dev set example:", dev_set[0])

    def test_custom_data_set_recommended(self):
        # Load data from the source
        data_frame = pd.read_csv("./data/custom_data_set.csv")

        # Formulate the loaded data into a Python list
        dataset = []
        for context, question, answer in data_frame.values:
            dataset.append(dspy.Example(context=context, question=question, answer=answer))
        pprint(dataset)

        self.assertEqual(2, len(dataset))

    def test_custom_data_set_advanced(self):
        # Using the Dataset class
        class CustomDataset(Dataset):
            def __init__(self, file_path, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                df = pd.read_csv(file_path)

                self._train = df.iloc[0:2].to_dict(orient='records')
                self._dev = df.iloc[2:].to_dict(orient='records')

        # Load the dataset
        dataset = CustomDataset("./data/custom_data_set.csv")
        print("Train dataset:", dataset.train)
        print("Dev dataset:", dataset.dev)

    def test_data_loader_from_huggingface(self):
        dl = DataLoader()

        # load all the data set
        data_set = dl.from_huggingface("HuggingFaceH4/CodeAlpaca_20K")
        print("All -> Train set: {}, Test set: {}".format(len(data_set["train"]), len(data_set["test"])))

        # load specific split
        data_set = dl.from_huggingface(
            "HuggingFaceH4/CodeAlpaca_20K",
            split=["train"]
        )
        print("Split -> Train set: {}".format(len(data_set["train"])))

        # load 10% of the specific split
        data_set_list = dl.from_huggingface(
            "HuggingFaceH4/CodeAlpaca_20K",
            split="train[:10%]"
        )
        print("Split -> Train 10% set: {}".format(len(data_set_list)))


if __name__ == '__main__':
    unittest.main()
