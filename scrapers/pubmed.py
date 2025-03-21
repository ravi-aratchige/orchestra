import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# add parent directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# load scraper utilities
from scrapers.utilities import set_up_driver, sanitize_pubmed_authors


def get_metadata_and_abstract(driver, search_str, article_number):
    """Get metadata (title and PMID) for the research paper
    obtained as the top result of searching on PubMed.

    Args:
        driver (WebDriver): the Chrome webdriver used to browse the web
        search_str (str): the search string used to retrieve research papers

    Returns:
        dict[str, int] | dict[str, Any]: a dictionary containing
        - research paper metadata (title and DOI)
        - the status code for the paper retrieval
    """

    # open the PubMed search page
    driver.get("https://pubmed.ncbi.nlm.nih.gov/")

    # locate search field and enter search query
    search_field = driver.find_element(
        By.XPATH,
        "/html/body/div[2]/main/div[1]/div/form/div/div[1]/div/span/input",
    )
    search_field.send_keys(search_str)
    search_field.send_keys(Keys.RETURN)
    time.sleep(3)

    # navigate to top search result
    try:
        results = driver.find_elements(By.CLASS_NAME, "docsum-title")
        if len(results) < article_number:
            return {
                "status": 404,
            }
        result = results[article_number - 1]
        result.click()
        time.sleep(5)
    except NoSuchElementException:
        return {
            "status": 404,
        }

    # get metadata and abstract of paper
    title = driver.find_element(By.CLASS_NAME, "heading-title").text
    pmid = driver.find_element(By.CLASS_NAME, "current-id").text
    authors = sanitize_pubmed_authors(
        driver.find_element(By.CLASS_NAME, "authors").text
    )
    abstract = driver.find_element(
        By.XPATH,
        "/html/body/div[5]/main/div[2]/div",
    ).text

    # NOTE
    # authors must be sanitized (as done above) as sometimes numbers can be found next to author names,
    # refering to their relevant university affiliation.

    return {
        "title": title,
        "pmid": pmid,
        "authors": authors,
        "abstract": abstract,
        "status": 200,
    }


def main():
    # set up the Chrome webdriver to visit websites
    driver = set_up_driver()

    # initialize search string for research paper(s)
    search_str = "transmucosal implant placement"

    # get metadata (title and PMID) based on first result from search
    result = get_metadata_and_abstract(driver, search_str, 1)

    if result["status"] == 404:
        print("Sorry, no research paper found!")
        print(f"STATUS: {result['status']}")
    elif result["status"] == 200:
        print(f"Found the following research paper:")
        print(f"Title: {result['title']}")
        print(f"PMID: {result['pmid']}")
        print(f"Authors: {result['authors']}")
        print(f"Abstract: {result['abstract']}")
        print(f"STATUS: {result['status']}")
    else:
        print(f"An unknown error has occured.")


if __name__ == "__main__":
    main()
