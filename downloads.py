import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOWNLOAD_DIR = "path_to_your_preferred_download_directory"  # Update this

def fetch_webpage_with_selenium(url):
    """
    Use Selenium to navigate the page and download specific files.
    """
    # Set up Chrome options for auto file download to specific directory
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        # Waiting for the table to load
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'table'))
        WebDriverWait(driver, 10).until(element_present)
        
        # Find the download links for `us-west` and `us-midwest`
        for region in ['us-west', 'us-midwest','us-northeast','us-south']:
            download_link = driver.find_element_by_partial_link_text(region)
            download_link.click()
            
            # Adding a wait to ensure files get enough time to start downloading
            driver.implicitly_wait(5)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

def downloader():
    url = 'https://batch.openaddresses.io/data'
    fetch_webpage_with_selenium(url)
    print(f"Files are downloaded to: {DOWNLOAD_DIR}")


