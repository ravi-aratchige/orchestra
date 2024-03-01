"""Orion parses search phrases from the user's queries.

Orion is part of the `researchers` package.
"""

import os
import sys
from langchain.prompts import PromptTemplate

# add parent directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# load researcher utilities
from researchers.utilities import configure_llm


def initialize_prompt_for_search_phrase_identification(query) -> str:
    # setup prompt template
    prompt_template = PromptTemplate.from_template(
        """You are Orion, a friendly and helpful AI chatbot in a team of AI chatbots who are assisting a user in medical research.

Your role is to understand the query asked by the user and parse a search phrase (or multiple search phrases) from it.

When separating the query into search phrase(s), add the word "AND" between search phrases if multiple search phrases
can be generated from the user's query.

Note: do not output anything except the search phrase(s). Do not add a full-stop after the search phrase(s).

Consider the following examples as reference:

Example 1:

Query: What studies have been done regarding transmucosal implant placement?
Search phrase(s): transmucosal implant placement

Example 2:

Query: What studies have been done by Gopal et. al. regarding mammogram analysis?
Search phrase(s): gopal AND mammogram analysis

Similarly, generate search phrase(s) for the following query:

Query: {query}
Search phrase(s):"""
    )

    # initialize prompt with user's query
    prompt = prompt_template.format(query=query)

    print(prompt)
    return prompt


def get_search_phrases(query) -> str:
    # set up LLM
    llm = configure_llm()

    # initialize prompt
    prompt = initialize_prompt_for_search_phrase_identification(
        query=(query),
    )

    # get search phrases using LLM
    search_phrases = llm.invoke(prompt)

    return search_phrases


def main():
    # initialize demo question
    query = "Tell me about genomic characterization in cancer genomes"

    # get search phrases for demo question
    search_phrases = get_search_phrases(query)

    print(f"Orion's output: {search_phrases}")


if __name__ == "__main__":
    main()
