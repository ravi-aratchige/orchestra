"""Maya performs inference based on the user's query and context retrieved by Stella.

Maya is part of the `researchers` package.
"""

import os
import sys
from langchain.prompts import PromptTemplate

# add parent directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# load researcher utilities
from researchers.utilities import configure_llm

# load Stella's functions
from researchers.stella import get_context


def initialize_prompt_for_response_generation(query):
    # setup prompt template
    prompt_template = PromptTemplate.from_template(
        """You are Maya, a friendly and helpful AI chatbot in a team of AI chatbots who are assisting a user in medical research.

Your role is answering queries about medical research. You have been asked the following query:

{query}

You must answer based on the following context:

{context}

---

Do not attempt to answer from your own knowledge. Provide citations in your answer using the information
provided in the above context.

Your response:"""
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
        query=query,
        context=context,
    )

    print(prompt)
    return prompt


def main():
    # set up LLM
    llm = configure_llm()

    # initialize prompt
    prompt = initialize_prompt_for_response_generation(
        query=("What studies have been done regarding transmucosal implant placement?")
    )

    # get output from model
    output = llm.invoke(prompt)
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
