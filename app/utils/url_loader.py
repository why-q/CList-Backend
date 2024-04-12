import re
from typing import Literal, Optional, Union

from selenium.webdriver import Chrome, Firefox


class URLLoader:
    def __init__(
        self,
        url: str,
        browser: Literal["firefox", "chrome"] = "chrome",
        headless: bool = True,
    ):
        try:
            import selenium  # noqa: F401
        except ImportError:
            raise ImportError(
                "selenium package not found, please install it with "
                "`pip install selenium`"
                " or "
                "`poetry add selenium`"
            )

        try:
            import unstructured  # noqa:F401
        except ImportError:
            raise ImportError(
                "unstructured package not found, please install it with "
                "`pip install unstructured`"
                " or "
                "`poetry add unstructured`"
            )

        self.url = url
        self.browser = browser
        self.headless = headless

    def _get_driver(self) -> Union["Chrome", "Firefox"]:
        if self.browser.lower() == "chrome":
            from selenium.webdriver import Chrome
            from selenium.webdriver.chrome.options import Options as ChromeOptions

            chrome_options = ChromeOptions()
            if self.headless:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")

            return Chrome(options=chrome_options)
        elif self.browser.lower() == "firefox":
            from selenium.webdriver import Firefox
            from selenium.webdriver.firefox.options import Options as FirefoxOptions

            firefox_options = FirefoxOptions()
            if self.headless:
                firefox_options.add_argument("--headless")
            return Firefox(
                options=firefox_options,
            )
        else:
            raise ValueError("Invalid browser specified. Use 'chrome' or 'firefox'.")

    def _get_type(self) -> str:
        if re.search(r"https://mp\.weixin\.qq\.com", self.url):
            return "wechat"
        else:
            return "others"

    def get_title(self) -> Optional[str]:
        driver = self._get_driver()
        driver.get(self.url)

        if (
            self._get_type() == "wechat"
            or driver.title is None
            or driver.title.strip() == ""
        ):
            from unstructured.partition.html import partition_html

            page_source = driver.page_source
            elements = partition_html(text=page_source)
            return str(elements[0])

        return driver.title
