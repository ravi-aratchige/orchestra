"""Stella retrieves context for Maya to perform inference.

Additionally, Stella can intelligently determine the number of articles to be retrieved for Maya,
based on the user's query.

Stella is part of the `researchers` package.
"""

import os
import sys
from langchain.prompts import PromptTemplate

# add parent directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# load scrapers
from scrapers.utilities import set_up_driver
from scrapers.pubmed import get_metadata_and_abstract

# load researcher functions and utilities
from researchers.utilities import configure_llm
from researchers.orion import decompose_query_into_search_phrases

# set default value for article count (when user's query is ambiguous)
DEFAULT_ARTICLE_COUNT = 3


def retrieve_context(search_phrases, query):
    """Stella's main function.

    This function retrieves context from PubMed for specified number of articles
    from search results.\n

    Default value for article count is set to 1, to ensure at least one article
    is retrieved for any scenario (unless specified otherwise).

    Args:
        search_phrase (str): string literal used for search on PubMed
        article_count (int): number of articles to be retrieved from search results

    Returns:
        str: Context required by Maya
    """

    print(
        f"INFO: Stella's main function ({retrieve_context.__name__}) has been invoked."
    )

    # set up driver for PubMed search
    driver = set_up_driver()

    # determine article count from user query
    article_count = calculate_article_count(query)

    context = ""

    # iterate through search results and add items to context
    for i in range(1, article_count + 1):
        search_result = get_metadata_and_abstract(driver, search_phrases, i)
        if search_result["status"] == 200:
            context += f"Title: {search_result['title']}\n"
            context += f"PMID: {search_result['pmid']}\n"
            context += f"Authors: {search_result['authors']}\n"
            context += f"Abstract: {search_result['abstract']}\n\n"
        elif search_result["status"] == 404:
            print(
                f"No result found for article {i} with search phrase '{search_phrases}'"
            )
        else:
            print(f"An unknown error occurred while retrieving article {i}")

    return context


def initialize_prompt_for_article_count_calculation(query):
    # set up prompt template
    prompt_template = PromptTemplate.from_template(
        """You are Stella, a friendly and helpful AI chatbot in a team of AI chatbots who are assisting a user in medical research.

When a user is conducting medical research with your help, literature must be retrieved from open-access sources to support
the responses provided by the team of AI chatbot to the user's queries. The literature thus retrieved will be provided to Maya,
another chatbot in your team, to perform inference and provide a meaningful response to the user's query.

Your role is to decide how many articles must be retrieved based on the user's query.

If the user has specified the number of articles required in their query itself, you must generate that number as an integer.

Note: do not generate the number as a word. For instance, 3 would a valid output, but "three" would not.

An example of this is given below:

Query: Give me five research papers about malignant brain tumors
Response: 5

Another similar example:

Query: I want 12 articles written by Gopal et. al.
Response: 12

If the user's query hints at one research paper, generate 1 as the output.

For example:

Query: Tell me about a research paper written about genomic characterization
Response: 1

For scenarios where the user's query doesn't specify any number, and Maya could benefit from having multiple research papers
to validate her answers, generate {default_article_count} as the output.

For example:

Query: What can you tell me about pancreas anatomy?
Response: {default_article_count}

Only generate the integer value as the output. Do not say anything else. Now analyze this query and decide the number of research papers necessary:

Query: {query}
Response:"""
    )

    # initialize prompt with user's query
    prompt = prompt_template.format(
        default_article_count=DEFAULT_ARTICLE_COUNT,
        query=(query),
    )

    return prompt


def calculate_article_count(query):
    # set up LLM
    llm = configure_llm()

    # calculate number of articles required
    prompt = initialize_prompt_for_article_count_calculation(query)
    print(prompt)

    # determine number of articles required
    try:
        article_count = int(llm.invoke(prompt))
    except ValueError:
        print(
            f"ERROR: Stella did not generate a valid integer! Defaulting to {DEFAULT_ARTICLE_COUNT} articles..."
        )
        article_count = DEFAULT_ARTICLE_COUNT

    print(
        f"Stella has determined that {article_count} articles are sufficient for this."
    )

    return article_count


def main():
    """Runs demo of Stella in action."""

    # initialize demo user query
    query = (
        "I want to know about research done regarding transmucosal implant placement"
    )

    # get search phrases and article count for demo query
    search_phrase = decompose_query_into_search_phrases(query)

    # retrieve context for relevant search
    context = retrieve_context(search_phrase, query)

    print(context)


if __name__ == "__main__":
    main()
