import unittest

import dspy
from dsp.utils import deduplicate
from dspy.datasets import HotPotQA
from dspy.evaluate import answer_exact_match, answer_passage_match, Evaluate
from dspy.teleprompt import BootstrapFewShot

from libs.dspy.utils.model import get_lm


class TestRag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the LM
        lm = get_lm()

        # Set up the retrieval model
        retrieval_model = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

        # Configure the DSPy
        dspy.settings.configure(lm=lm, rm=retrieval_model)

        # Load the dataset
        dataset = HotPotQA(train_seed=1, train_size=20, eval_seed=2023, dev_size=50, test_size=0)

        # Tell DSPy that the 'question' field is the input. Any other fields are labels and/or metadata.
        cls.train_set = [x.with_inputs('question') for x in dataset.train]
        cls.dev_set = [x.with_inputs('question') for x in dataset.dev]

    def test_data_set(self):
        # Research the train_set
        train_example = self.train_set[0]

        print(f"\n\nTrain example: {train_example}")
        print(f"Question: {train_example.question}")
        print(f"Answer: {train_example.answer}")

        # Research the dev_set
        dev_example = self.dev_set[18]

        print(f"\n\nDev example: {dev_example}")
        print(f"Question: {dev_example.question}")
        print(f"Answer: {dev_example.answer}")
        print(f"Relevant Wikipedia Titles: {dev_example.gold_titles}")

    def test_single_search_query(self):
        # Define the signature
        class GenerateAnswer(dspy.Signature):
            """Answer questions with short factoid answers."""

            context = dspy.InputField(desc="may contain relevant facts")
            question = dspy.InputField()

            answer = dspy.OutputField(desc="often between 1 and 5 words")

        # Build the Pipeline as a DSPy module
        class RagProgram(dspy.Module):

            def __init__(self, num_passages=3):
                super().__init__()

                self.retrieve = dspy.Retrieve(k=num_passages)
                self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

            def forward(self, question):
                # search for the top-num_passages relevant passages
                context = self.retrieve(question).passages

                # generate the answer
                prediction = self.generate_answer(context=context, question=question)

                # return the answer
                return dspy.Prediction(context=context, answer=prediction.answer)

        # Optimize the Pipeline

        # Validation logic: check that the predicted answer is correct.
        # Also check that the retrieved context does actually contain that answer.
        def validate_context_and_answer(example, pred, trace=None):
            answer_em = answer_exact_match(example, pred)
            answer_pm = answer_passage_match(example, pred)
            return answer_em and answer_pm

        # Set up a basic teleprompter, which will compile our RAG program.
        teleprompter = BootstrapFewShot(metric=validate_context_and_answer)

        # Compile the RAG program
        compiled_rag = teleprompter.compile(RagProgram(), trainset=self.train_set)

        # Ask any question you like to this simple RAG program.
        my_question = "What castle did David Gregory inherit?"

        # Get the prediction. This contains `pred.context` and `pred.answer`.
        prediction = compiled_rag(my_question)

        # Print the contexts and the answer.
        print(f"Question: {my_question}")
        print(f"Predicted Answer: {prediction.answer}")
        print(f"Retrieved Contexts (truncated): {[c[:200] + '...' for c in prediction.context]}")

        # Inspect the last prompt for the LM
        dspy.settings.lm.inspect_history(n=1)

        # Evaluating the Pipeline

        # Set up the `evaluate_on_hotpot_qa` function. We'll use this many times below.
        evaluate_on_hotpot_qa = Evaluate(
            devset=self.dev_set,
            num_threads=1,
            display_progress=False,
            display_table=5
        )

        # Evaluate the `compiled_rag` program with the `answer_exact_match` metric.
        metric = answer_exact_match
        evaluate_on_hotpot_qa(compiled_rag, metric=metric)

        # Evaluating the Retrieval
        def gold_passages_retrieved(example, pred, trace=None):
            gold_titles = set(map(dspy.evaluate.normalize_text, example['gold_titles']))
            found_titles = set(map(dspy.evaluate.normalize_text, [c.split(' | ')[0] for c in pred.context]))

            return gold_titles.issubset(found_titles)

        compiled_rag_retrieval_score = evaluate_on_hotpot_qa(compiled_rag, metric=gold_passages_retrieved)

    def test_multi_hop_question_answering(self):
        class GenerateAnswer(dspy.Signature):
            """Answer questions with short factoid answers."""

            context = dspy.InputField(desc="may contain relevant facts")
            question = dspy.InputField()

            answer = dspy.OutputField(desc="often between 1 and 5 words")

        class GenerateSearchQuery(dspy.Signature):
            """Write a simple search query that will help answer a complex question"""

            context = dspy.InputField(desc="may contain relevant facts")
            question = dspy.InputField()

            query = dspy.OutputField()

        class SimplifiedBaleenProgram(dspy.Module):
            def __init__(self, passages_per_hop=3, max_hops=2):
                super().__init__()

                # For each hop, we will have one dspy.ChainOfThought predictor with the GenerateSearchQuery signature.
                self.generate_query = [dspy.ChainOfThought(GenerateSearchQuery) for _ in range(max_hops)]

                # The module will conduct the search using the generated queries the Retrieve model.
                self.retrieve = dspy.Retrieve(k=passages_per_hop)

                # The dspy.ChainOfThought module will be used with the GenerateAnswer signature to produce the answer.
                self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

                self.max_hops = max_hops

            def forward(self, question):
                # context accumulator
                context = []

                for hop in range(self.max_hops):
                    # generate a search query using the predictor at self.generate_query[hop].
                    query = self.generate_query[hop](context=context, question=question).query

                    # retrieve the top-k passages using the query
                    passages = self.retrieve(query).passages

                    # add the (deduplicated) passages to the context accumulator
                    context = deduplicate(context + passages)

                # use self.generate_answer to produce an answer
                prediction = self.generate_answer(context=context, question=question)

                # return the prediction with the retrieved context and predicted answer.
                return dspy.Prediction(context=context, answer=prediction.answer)

        def validate_context_and_answer_and_hops(example, prediction, trace=None):
            if not dspy.evaluate.answer_exact_match(example, prediction):
                return False

            if not dspy.evaluate.answer_passage_match(example, prediction):
                return False

            hops = [example.question] + [outputs.query for *_, outputs in trace if 'query' in outputs]

            if max([len(h) for h in hops]) > 100:
                return False

            if any(dspy.evaluate.answer_exact_match_str(hops[idx], hops[:idx], frac=0.8) for idx in
                   range(2, len(hops))):
                return False

            return True

        # Executing the Pipeline

        # Ask any question you like to this simple RAG program.
        my_question = "How many storeys are in the castle that David Gregory inherited?"

        # Get the prediction. This contains `pred.context` and `pred.answer`.
        uncompiled_baleen = SimplifiedBaleenProgram()  # uncompiled (i.e., zero-shot) program
        pred = uncompiled_baleen(my_question)

        # Print the contexts and the answer.
        print(f"Question: {my_question}")
        print(f"Predicted Answer: {pred.answer}")
        print(f"Retrieved Contexts (truncated): {[c[:200] + '...' for c in pred.context]}")

        # Set up a basic teleprompter, which will compile our RAG program.
        teleprompter = BootstrapFewShot(metric=validate_context_and_answer_and_hops)

        # Compile the RAG program
        compiled_baleen = teleprompter.compile(
            SimplifiedBaleenProgram(),
            teacher=SimplifiedBaleenProgram(passages_per_hop=2),
            trainset=self.train_set)

        # Execute this program
        pred = compiled_baleen(my_question)

        # Get the prediction. This contains `pred.context` and `pred.answer`.

        # Print the contexts and the answer.
        print(f"Question: {my_question}")
        print(f"Predicted Answer: {pred.answer}")
        print(f"Retrieved Contexts (truncated): {[c[:200] + '...' for c in pred.context]}")

        dspy.settings.lm.inspect_history(n=3)

        # Evaluating the Pipeline

        # Define metric to check if we retrieved the correct documents
        def gold_passages_retrieved(example, prediction, trace=None):
            gold_titles = set(map(dspy.evaluate.normalize_text, example["gold_titles"]))
            found_titles = set(
                map(dspy.evaluate.normalize_text, [c.split(" | ")[0] for c in prediction.context])
            )
            return gold_titles.issubset(found_titles)

        # Set up the `evaluate_on_hotpot_qa` function. We'll use this many times below.
        evaluate_on_hotpot_qa = Evaluate(
            devset=self.dev_set,
            num_threads=1,
            display_progress=True,
            display_table=5
        )

        uncompiled_baleen_retrieval_score = evaluate_on_hotpot_qa(
            uncompiled_baleen,
            metric=gold_passages_retrieved,
            display=False)

        compiled_baleen_retrieval_score = evaluate_on_hotpot_qa(compiled_baleen, metric=gold_passages_retrieved)

        print(f"## Retrieval Score for uncompiled Baleen: {uncompiled_baleen_retrieval_score}")
        print(f"## Retrieval Score for compiled Baleen: {compiled_baleen_retrieval_score}")


if __name__ == '__main__':
    unittest.main()
