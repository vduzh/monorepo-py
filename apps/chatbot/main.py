from operator import itemgetter
from pprint import pprint

from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


def main():
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(memory_key="messages", return_messages=True)

    # system_template = "You are a chatbot specializing {subject}."
    system_template = "You are a helpful assistant."
    human_template = "{content}"
    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            MessagesPlaceholder(variable_name="messages"),
            # ("human", human_template)
            HumanMessagePromptTemplate.from_template(human_template)
        ]
    )

    chain = (
        RunnablePassthrough.assign(
            messages=RunnableLambda(memory.load_memory_variables) | itemgetter("messages")
        )
        | chat_prompt_template
        | llm
    )

    while True:
        content = input("User: ")
        if content == "exit":
            break

        inputs = {"content": content}
        message = chain.invoke(inputs)

        print("AI:", message.content)
        memory.save_context(inputs, {"output": message.content})


if __name__ == "__main__":
    main()
