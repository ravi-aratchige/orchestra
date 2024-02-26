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
