"""Titan is the primary research manager of Orchestra.

Titan is part of the `managers` package.
"""

import os
import sys

# add parent directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# load researcher functions and utilities
from researchers.orion import decompose_query_into_search_phrases
from researchers.stella import retrieve_context
from researchers.maya import generate_response


def basic_search_and_retrieve_operation(query) -> str:
    # decompose user query into search phrases (Orion)
    search_phrases = decompose_query_into_search_phrases(query)

    # retrieve context from Stella
    context = retrieve_context(
        search_phrases=search_phrases,
        query=query,
    )

    # perform inference with Maya using retrieved context and user query
    response = generate_response(
        context=context,
        query=query,
    )

    return response


def main():
    """Runs demo of Titan in action."""

    # initialize demo query
    query = "What studies have been done regarding transmucosal implant placement?"

    # get response for demo query
    output = basic_search_and_retrieve_operation(query)

    print(output)


if __name__ == "__main__":
    main()
