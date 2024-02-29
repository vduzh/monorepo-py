# import argparse

from dotenv import load_dotenv

# from langchain.chains import LLMChain, SequentialChain
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


def main():
    while True:
        content = input(">> ")
        if content == "exit":
            break

        print(f"You entered: {content}")
    pass

    # extract app arguments from the command line
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--language", default="python")
    # parser.add_argument("--task", default="return a list of numbers")
    #
    # args = parser.parse_args()
    #
    # language = args.language
    # task = args.task
    #
    # print("== INPUT ==")
    # print("Language:", language)
    # print("Task:", task, end="\n\n")

    # build the chain
    # llm = ChatOpenAI()
    #
    # code_chain = LLMChain(
    #     llm=llm,
    #     prompt=PromptTemplate.from_template("Write a {language} function that will {task}."),
    #     output_key="code"
    # )
    #
    # test_chain = LLMChain(
    #     llm=llm,
    #     prompt=PromptTemplate.from_template("Write a unit-test for the following {language} code: {code}"),
    #     output_key="test"
    # )
    #
    # chain = SequentialChain(
    #     chains=[code_chain, test_chain],
    #     input_variables=["language", "task"],
    #     output_variables=["code", "test"],
    # )
    #
    # out = chain.invoke({"language": language, "task": task})
    # print(">>>>>>>> GENERATED CODE:", out["code"], sep="\n", end="\n\n")
    # print(">>>>>>>> GENERATED TEST:", out["test"], sep="\n", end="\n\n")


if __name__ == "__main__":
    main()
