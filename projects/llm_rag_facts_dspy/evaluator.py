import os

import dspy
from dspy.evaluate import Evaluate

from projects.llm_rag_facts_dspy.config.dataset import get_devset
from projects.llm_rag_facts_dspy.config.lm import get_lm
from projects.llm_rag_facts_dspy.config.metric import get_metric
from projects.llm_rag_facts_dspy.config.rm import get_rm
from projects.llm_rag_facts_dspy.programs.rag_program import RagProgram


def main():
    print("evaluator app started\n")

    with dspy.context(lm=get_lm(), rm=get_rm()):
        # Load optimized program
        program = RagProgram()
        program.load(path=os.path.relpath(f"data/{program.name}.json"))

        # Set up the evaluator, which can be used multiple times.
        evaluate = Evaluate(
            devset=get_devset(),
            metric=get_metric(),
            num_threads=4,
            display_progress=True,
            display_table=0
        )

        # Evaluate the program
        evaluate(program)


if __name__ == "__main__":
    main()
