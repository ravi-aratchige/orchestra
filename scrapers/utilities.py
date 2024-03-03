"""Contains utilities to be used by scrapers.\n

e.g. Setting up WebDriver, sanitizing scraped data etc.
"""

import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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


def sanitize_pubmed_authors(authors):
    """Sanitize a list of PubMed article authors by
    - Removing numbers (references to the institutional affiliations of the authors)
    - Removing whitespace left beside the numbers

    Args:
        authors (str): a unsanitized string of authors, separated by commas

    Returns:
        str: a sanitized string of authors
    """

    # remove numbers
    authors = re.sub(r"\d+", "", authors)

    # remove additional spaces (added by whitespace next to numbers)
    sanitized_authors = re.sub("   ", "", authors)

    return sanitized_authors


if __name__ == "__main__":
    pass
