import os

import dspy
from dspy.teleprompt import BootstrapFewShot

from projects.llm_rag_facts_dspy.config.dataset import get_trainset
from projects.llm_rag_facts_dspy.config.lm import get_lm
from projects.llm_rag_facts_dspy.config.metric import validate_context_and_answer
from projects.llm_rag_facts_dspy.config.rm import get_rm
from projects.llm_rag_facts_dspy.programs.rag_program import RagProgram


class Optimizer:
    def __init__(self, program, teleprompter, trainset, path):
        super().__init__()

        self._program = program
        self._teleprompter = teleprompter
        self._trainset = trainset
        self._path = path

    def __call__(self, *args, **kwargs):
        # Optimize the program
        optimized_program = self._teleprompter.compile(self._program, trainset=self._trainset)

        # Save the optimized program to a file
        optimized_program.save(self._path)


def main():
    print("optimizer app started \n")

    with dspy.context(lm=get_lm(), rm=get_rm()):
        # Set up a  teleprompter
        teleprompter = BootstrapFewShot(metric=validate_context_and_answer)

        # Create program
        program = RagProgram()

        # Create the optimizer and call it
        optimizer = Optimizer(
            program,
            teleprompter,
            get_trainset(),
            os.path.join(os.path.dirname(__file__), "data", f"{program.name}.json")
        )
        optimizer()


if __name__ == "__main__":
    main()
