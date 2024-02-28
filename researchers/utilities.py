import os
from dotenv import load_dotenv
from langchain_community.llms import Cohere


def configure_llm():
    # load Cohere API key
    load_dotenv()
    os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")

    # configure LLM
    llm = Cohere(
        model="command-xlarge-nightly",
        temperature=0.5,
        max_tokens=800,
        k=0,
        p=1,
    )

    return llm


if __name__ == "__main__":
    pass
