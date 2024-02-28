"""Maya performs inference based on the user's query and context retrieved by Stella.
"""

import os
import sys
from langchain.prompts import PromptTemplate
from .utilities import configure_llm

# load scrapers
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from scrapers.utilities import set_up_driver
from scrapers.pubmed import get_metadata_and_abstract


def get_context(search_phrase, article_count):
    driver = set_up_driver()
    context = ""

    for i in range(1, article_count):
        search_result = get_metadata_and_abstract(driver, search_phrase)
        pass


def initialize_prompt(question):
    # setup prompt template
    prompt_template = PromptTemplate.from_template(
        """You are Maya, a friendly and helpful AI chatbot who is proficient
    in answering queries about medical research. You have been asked the following question:

    {question}

    You must answer based on the following context:

    {context}

    ---

    Do not attempt to answer from your own knowledge. Provide citations in your answer using the information
    provided in the above context.

    Your response:
    """
    )

    # initialize inputs
    search_phrase = "transmucosal implant placement"
    driver = set_up_driver()
    search_result = get_metadata_and_abstract(driver, search_phrase)
    context = f"""Title: {search_result["title"]}
    PMID: {search_result['pmid']}
    Authors: {search_result['authors']}
    Abstract: {search_result['abstract']}
    """

    # initialize prompt with inputs
    prompt = prompt_template.format(
        question=question,
        context=context,
    )

    print(prompt)
    return prompt


def main():
    # set up LLM
    llm = configure_llm()

    # initialize prompt
    prompt = initialize_prompt(
        question=(
            "What is the name of the study done regarding transmucosal implant placement?"
        )
    )

    # get output from model
    output = llm(prompt)
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
