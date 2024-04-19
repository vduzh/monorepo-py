import unittest

import dspy


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


if __name__ == '__main__':
    unittest.main()
