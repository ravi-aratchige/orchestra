import os
from dotenv import load_dotenv
from langchain_community.llms import Cohere


def configure_llm():
    """Configure and return an instance of an LLM for researchers to use.

    Returns:
        langchain_community.llms: LLM instance providing connectivity to remotely-hosted large language models
    """
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
