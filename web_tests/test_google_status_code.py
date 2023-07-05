import requests
import bs4
from lxml import etree
import pytest
import os

output_dir = os.environ.get("OUTPUT_DIR", "/app/data")
output_file = os.path.join(output_dir, "web_tests_results/test_qoogle_status_output.xml")


links = ['https://www.google.com/', 'https://www.youtube.com/']

@pytest.fixture
def links_fixture():
    return links

def test_status_codes(links_fixture):
    root = etree.Element("data")
    for site in links_fixture:
        resp = requests.get(site)
        assert resp.status_code == 200
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        site_name = soup.title.string
        print(f'\nСтатус код для {site_name}, ссылка: {site}')
        print(resp.status_code)


        site_element = etree.SubElement(root, "site")
        name_element = etree.SubElement(site_element, "name")
        name_element.text = site_name
        url_element = etree.SubElement(site_element, "url")
        url_element.text = site
        status_element = etree.SubElement(site_element, "status")
        status_element.text = str(resp.status_code)

    tree = etree.ElementTree(root)
    tree.write("web_tests_results\\test_qoogle_status_output.xml", pretty_print=True)



