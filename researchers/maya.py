import os
import sys
from dotenv import load_dotenv
from langchain_community.llms import Cohere
from langchain.prompts import PromptTemplate

# load scrapers
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from scrapers.utilities import set_up_driver
from scrapers.pubmed import get_metadata_and_abstract

# load Cohere API key
load_dotenv()
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")

# configure LLM
llm = Cohere(model="command-xlarge-nightly", temperature=0.5, max_tokens=800, k=0, p=1)

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
question = (
    "What is the name of the study done regarding transmucosal implant placement?"
)
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

# get output from model
output = llm(prompt)
print(output)
