from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os


def setup():
    global driver, download_dir
    options = webdriver.ChromeOptions()
    download_dir = "/app/tmp"
    os.makedirs(download_dir, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=options
    )
    return driver


def get_new_file(newfilename):
    target = "/app/downloads"
    os.makedirs(target, exist_ok=True)

    def has_files(directory):
        return any(os.path.isfile(
            os.path.join(directory, f)) for f in os.listdir(directory))

    while not has_files(download_dir):
        time.sleep(0.5)

    file = os.listdir(download_dir)[0]

    while "crdownload" in file:
        time.sleep(0.5)
        file = os.listdir(download_dir)[0]
    os.rename(os.path.join(download_dir, file),
              os.path.join(target, f"file_{newfilename}_{file}"))
    print(f"file_{newfilename}_{file}")
    return downloaded_files.append(f"file_{newfilename}_{file}")


def download_igc_file(url: str):
    driver.get(url)
    time.sleep(2)
    try:
        igc_file = driver.find_element(By.XPATH, "//*[@id='IgcDownloadPos']")
    except Exception:
        time.sleep(5)
        igc_file = driver.find_element(By.XPATH, "//*[@id='IgcDownloadPos']")
    igc_file.click()
    time.sleep(1)

    iframe = driver.find_element(By.ID, "IgcDownloadFrame")
    driver.switch_to.frame(iframe)
    target = driver.find_element(
        By.XPATH,
        "//*[@id='captchaWrapper']/div[5]/div").value_of_css_property(
            "background-position")
    target = target.split("px ")[0]

    dragableobjects = driver.find_elements(
        By.CSS_SELECTOR, "[id^='draggable']")
    for obj in dragableobjects:
        obj_pos = obj.value_of_css_property(
            "background-position").split("px ")[0]
        if target == obj_pos:
            obj.click()
            downloadfile = driver.find_element(By.ID, "igcLink")
            downloadfile.click()
            break
    time.sleep(1)
    get_new_file(url.split("/")[-1])


def main(url: str):
    global downloaded_files
    downloaded_files = []
    setup()
    driver.get(url)
    time.sleep(2)
    link_elements = driver.find_elements(By.CSS_SELECTOR, "[id^='row_']")

    links = [link_element.find_element(
        By.CLASS_NAME, "flightlink").get_attribute("href")
        for link_element in link_elements]

    if len(links) > 10:
        links = links[:10]
    for link in links:
        print(link)
        time.sleep(1)
        if link:
            try:
                download_igc_file(link)
            except Exception:
                print(f"Failed to download {link}")
                continue
    driver.quit()
    return downloaded_files


if __name__ == "__main__":
    url = "https://www.ypforum.com/leonardo/tracks/world/2025.05/brand:all,cat:1,class:all,xctype:all,club:all,pilot:0_6573,takeoff:all"

    main(url)
