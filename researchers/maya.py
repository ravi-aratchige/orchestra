"""Maya performs inference based on the user's query and context retrieved by Stella.
"""

import os
import sys
from langchain.prompts import PromptTemplate

# add parent directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# load researcher utilities
from researchers.utilities import configure_llm

# load Stella
from researchers.stella import get_context


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

    # initialize search phrase and article count (for context retrieval)
    search_phrase = "transmucosal implant placement"
    article_count = 3

    # load context from Stella
    context = get_context(
        search_phrase,
        article_count,
    )

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
            "What studies have been done regarding transmucosal implant placement?"
        )
    )

    # get output from model
    output = llm.invoke(prompt)
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
