"""Stella retrieves context for Maya to perform inference.
"""

import os
import sys

# add parent directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# load scrapers
from scrapers.utilities import set_up_driver
from scrapers.pubmed import get_metadata_and_abstract


def get_context(search_phrase, article_count=1):
    """Retrieve context from PubMed for specified number of articles
    from search results.\n

    Default value for article count is set to 1, to ensure at least one article
    is retrieved for any scenario (unless specified otherwise).

    Args:
        search_phrase (str): string literal used for search on PubMed
        article_count (int): number of articles to be retrieved from search results

    Returns:
        str: Context required by Maya
    """
    driver = set_up_driver()
    context = ""

    for i in range(1, article_count + 1):
        search_result = get_metadata_and_abstract(driver, search_phrase, i)
        if search_result["status"] == 200:
            context += f"Title: {search_result['title']}\n"
            context += f"PMID: {search_result['pmid']}\n"
            context += f"Authors: {search_result['authors']}\n"
            context += f"Abstract: {search_result['abstract']}\n\n"
        elif search_result["status"] == 404:
            print(
                f"No result found for article {i} with search phrase '{search_phrase}'"
            )
        else:
            print(f"An unknown error occurred while retrieving article {i}")

    return context


def main():
    # configure inputs for context retrieval
    search_phrase = "transmucosal implant placement"
    article_count = 3

    # retrieve context for relevant search
    context = get_context(search_phrase, article_count)

    print(context)


if __name__ == "__main__":
    main()
