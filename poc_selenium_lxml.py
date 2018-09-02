import contextlib
import os
import sys

from lxml import html

from selenium import webdriver
from selenium.webdriver.chrome import options


class Crawler(object):
    def __init__(self):
        self.extracted_data = {}
        self.selectors = {}

    def crawl(self):
        with self.driver_cm(webdriver.Chrome,
                            chrome_options=self.create_chrome_options()) as driver:
            self.driver = driver
            self.crawl_execution()

    def crawl_execution(self):
        self.driver.get(self.url)
        tree = html.fromstring(self.driver.page_source)

        for name, selectors in self.selectors.items():

            for selector in selectors:
                content = tree.xpath(selector)

                if content:
                    if not self.extracted_data.get(name):
                        self.extracted_data[name] = []

                    for element in content:
                        self.extracted_data[name].append(element.text_content())

    @classmethod
    def create_chrome_options(cls, proxy_url=None):
        driver_options = options.Options()

        if not os.environ.get('DISABLE_HEADLESS'):
            driver_options.add_argument("--headless")
            driver_options.add_argument("--no-sandbox")

        driver_options.add_argument("--disable-notifications")
        driver_options.add_argument("--disable-extensions")

        if proxy_url:
            driver_options.add_argument('--proxy-server=%s' % proxy_url)

        return driver_options

    @contextlib.contextmanager
    def driver_cm(self, webdriver_class, *args, **kwargs):
        driver = webdriver_class(*args, **kwargs)
        try:
            driver.implicitly_wait(2)
            yield driver
        finally:
            driver.quit()

    def parse(self, unparsed_data):
        data = unparsed_data.split("\n")[:-1]

        for line in data:
            name, *selector = line.split(",")
            self.selectors[name] = selector

    def read_input(self):
        self.url = sys.argv[2]

        with open(sys.argv[1]) as infile:
            self.data = self.parse(infile.read())


def main():
    crawler = Crawler()
    crawler.read_input()
    crawler.crawl()

    print(crawler.extracted_data)


if __name__ == "__main__":
    main()
