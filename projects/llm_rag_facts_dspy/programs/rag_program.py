# Define the signature
import dspy


class GenerateAnswer(dspy.Signature):
    """Answer questions with short factoid answers."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()

    answer = dspy.OutputField(desc="often between 1 and 5 words")


# Build the Pipeline as a DSPy module
class RagProgram(dspy.Module):
    name = "rag_program"

    def __init__(self, num_passages=3):
        super().__init__()

        # create a retriever
        self.retrieve = dspy.Retrieve(k=num_passages)

        # create an object to call llm
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        # search for the top-num_passages relevant passages
        context = self.retrieve(question).passages

        # generate the answer
        prediction = self.generate_answer(context=context, question=question)

        # return the answer
        return dspy.Prediction(context=context, answer=prediction.answer)
