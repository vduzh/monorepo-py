import os

import dspy

from projects.llm_rag_facts_dspy.config.lm import get_lm
from projects.llm_rag_facts_dspy.programs.rag_program import RagProgram
from projects.llm_rag_facts_dspy.config.rm import get_rm


def main():
    print("main app started\n")

    with dspy.context(lm=get_lm(), rm=get_rm()):
        # Load optimized program
        program = RagProgram()
        # program.load(path=os.path.join(os.path.dirname(__file__), "data", f"{program.name}.json"))

        while True:
            question = input("Enter your question or exit: ")

            # Check fot exit the app
            if "exit" == question:
                break

            # Call the program with input argument for inference.
            prediction = program(question=question)

            # Show the result
            print(f"Answer: {prediction.answer}\n\n")


if __name__ == "__main__":
    main()
