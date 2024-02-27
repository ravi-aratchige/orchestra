I need agents for the following tasks primarily:

1. Understanding what the user wants. Are they asking a question that needs to be broken into search strings? Are they asking about something that happened in the conversation previously?
2. Breaking the user's question into search strings properly, then checking the semantic similarity between the search results retrieved and the user's question to re-rank the search results and get the most relevant search result
3. Retrieving context from the re-ranked search result(s) and getting an LLM's output using the retrieved context.