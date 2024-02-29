from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


def main():
    llm = ChatOpenAI()

    # system_template = "You are a chatbot specializing {subject}."
    human_template = "{content}"
    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            # ("system", system_template),
            ("human", human_template)
        ]
    )

    chain = chat_prompt_template | llm

    while True:
        content = input("User: ")
        if content == "exit":
            break

        message = chain.invoke({"content": content})
        print("AI:", message.content)


if __name__ == "__main__":
    main()
