import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def set_up_driver():
    """Set up a Chrome webdriver to browse the web.

    Returns:
        WebDriver: the Chrome webdriver
    """
    # ensure browser does not close after end of script execution
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # set download path for PDFs
    download_dir = "/home/ravindu-aratchige/Downloads"
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        },
    )

    # set up the Chromium web driver
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_paper_metadata(driver, search_str):
    """Get metadata (title and DOI) for the research paper
    obtained as the top result of searching on CrossRef.

    Args:
        driver (WebDriver): the Chrome webdriver used to browse the web
        search_str (str): the search string used to retrieve research papers

    Returns:
        dict[str, str]: a dictionary containing research paper metadata (title and DOI)
    """
    # open the Crossref webpage
    driver.get("https://search.crossref.org/")
    time.sleep(5)

    # locate search field and enter search query
    search_field = driver.find_element(By.ID, "search-input")
    search_field.send_keys(search_str)
    search_field.send_keys(Keys.RETURN)
    time.sleep(10)

    # get title and DOI for top result
    result = driver.find_element(By.TAG_NAME, "tr")
    title = result.find_element(By.CLASS_NAME, "lead").text
    links_section = result.find_element(By.CLASS_NAME, "item-links")
    doi = links_section.find_element(By.TAG_NAME, "a").text.replace(
        "https://doi.org/", ""
    )
    print(f"Title: {title}")
    print(f"DOI: {doi}")

    return {
        "title": title,
        "doi": doi,
    }


def download_paper(driver, metadata):
    """Download a selected research paper (from SciHub)
    into the disk (to system "Downloads" folder).

    Args:
        driver (WebDriver): the Chrome webdriver needed to visit the SciHub webpage
        metadata (dict[str, str]): the metadata of the research paper to be downloaded
    """
    # open SciHub
    # try:
    #     driver.get("https://sci-hub.wf/")
    #     scihub_search_field = driver.find_element(By.NAME, "request")
    # except NoSuchElementException:
    #     driver.get("https://sci-hub.se/")
    #     scihub_search_field = driver.find_element(By.ID, "request")
    # finally:
    #     scihub_search_field.send_keys(metadata["doi"])
    #     scihub_search_field.send_keys(Keys.RETURN)

    driver.get("https://sci-hub.se/")
    scihub_search_field = driver.find_element(By.ID, "request")

    scihub_search_field.send_keys(metadata["doi"])
    scihub_search_field.send_keys(Keys.RETURN)

    # wait for download to complete
    time.sleep(10)


def main():
    # set up the Chrome webdriver to visit websites
    driver = set_up_driver()

    # initialize search string for research paper(s)
    search_str = "transmucosal implant placement"

    # get metadata (title and DOI) based on first result from search
    paper_metadata = get_paper_metadata(driver, search_str)

    # download paper to local disk
    download_paper(driver, metadata=paper_metadata)
    pass


if __name__ == "__main__":
    main()
