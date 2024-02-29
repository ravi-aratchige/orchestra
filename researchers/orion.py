"""Orion parses search phrases from the user's queries.
"""

import os
import sys
from click import prompt
from langchain.prompts import PromptTemplate

# add parent directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# load researcher utilities
from researchers.utilities import configure_llm


def initialize_prompt(question):
    # setup prompt template
    prompt_template = PromptTemplate.from_template(
        """You are Orion, a friendly and helpful AI chatbot in a team of AI chatbots who are assisting a user in medical research.

Your role is to understand the question asked by the user and parse a search phrase (or multiple search phrases) from it.

When separating the question into search phrase(s), add the word "AND" between search phrases if multiple search phrases
can be generated from the user's question.

Note: do not output anything except the search phrase(s). Do not add a full-stop after the search phrase(s).

Consider the following examples as reference:

Example 1:

Question: What studies have been done regarding transmucosal implant placement?
Search phrase(s): transmucosal implant placement

Example 2:

Question: What studies have been done by Gopal et. al. regarding mammogram analysis?
Search phrase(s): gopal AND mammogram analysis

Similarly, generate search phrase(s) for the following question:

Question: {question}
Search phrase(s):"""
    )

    # initialize prompt with input question
    prompt = prompt_template.format(question=question)

    print(prompt)
    return prompt


def main():
    # set up LLM
    llm = configure_llm()

    # initialize prompt
    prompt = initialize_prompt(
        question=("Tell me about genomic characterization in cancer genomes")
    )

    # get search phrases using LLM
    output = llm.invoke(prompt)
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
