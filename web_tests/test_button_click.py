import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import xml.etree.ElementTree as ET

links = ['https://www.google.com/', 'https://www.youtube.com/']

@pytest.fixture
def links_fixture():
    return links

def test_click_buttons(links_fixture):
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)
    root = ET.Element("test_results")
    for site in links_fixture:
        site_element = ET.SubElement(root, "site")
        site_element.set("url", site)
        resp = requests.get(site)
        soup = BeautifulSoup(resp.text, 'lxml')
        buttons = soup.find_all('a')
        driver.get(site)
        success_count = 0
        fail_count = 0
        for button in buttons:
            button_element = ET.SubElement(site_element, "button")
            button_text = button.text
            button_element.set("text", button_text)
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{button_text}')]")))
                button_element_ = driver.find_element(By.XPATH, f"//a[contains(text(), '{button_text}')]")
                button_element_.click()
                success_count += 1
                status_code = driver.execute_script('return document.readyState;')
                button_element.set("status_code", status_code)
                button_element.set("success", "true")
                driver.back()
            except Exception as e:
                fail_count += 1
                button_element.set("success", "false")
                button_element.set("error", str(e))
        site_element.set("success_count", str(success_count))
        site_element.set("fail_count", str(fail_count))
    tree = ET.ElementTree(root)
    tree.write("web_tests_results\\test_results.xml")
    driver.quit()
