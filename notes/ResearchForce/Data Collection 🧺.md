## Searching

Currently, we have two approaches for searching literature:

1. Searching using search strings on Google Scholar, then scraping the title(s) and searching for them on Crossref for metadata (DOI)
2. Searching directly on Crossref

Both methods do not have any hindrance on scraping. Both methods seem to yield effective results.

However, with Google Scholar, we get a preview of some (or all) of our search strings appearing in the literature.

![[Pasted image 20240213013540.png]]

This might be useful for performing semantic re-ranking of search results.

<a href="https://arxiv.org/">arxiv.org</a> is not a good place for search, as it has a bad search engine, and usually doesn't have literature close to our search string anyways.

## Getting Metadata

Getting metadata (usually the DOI number) can be done by running a Selenium script to search for the relevant literature on Crossref. This is effective most of the time.

Even if the exact literature is not found, Crossref will get the closest one possible (need to add logging to check whether Crossref got the same literature as provided as input to it during search).

## Retrieving Papers

This is the tricky part. How do we get research papers in a way that we can scrape data from them to ingest into the RAG pipeline?

For medical research purposes, we can use Pubmed. Pubmed has a moderately good search engine, and almost all of the search results have abstracts (filters can also be applied to exclude literature without abstracts). This means, instead of reading through full literature,  we can rely on the abstracts of medical research.

But we need to check the feasibility of this (whether we can rely on the abstracts only to produce good responses).