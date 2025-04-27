from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from autoparse.tools.fetchers.static_fetcher import fetch_static_html


def fetch_dynamic_html(
    url: str,
    timeout: int = 10,
    headless: bool = True,
    window_size: str = "1920,1080"
) -> str:
    """
    Fetch HTML from a dynamic site by rendering with headless Chrome.

    Args:
        url: target URL
        timeout: how many seconds to wait for page load
        headless: whether to run browser in headless mode
        window_size: browser window size, e.g. "1920,1080"

    Returns:
        rendered HTML as a string

    Raises:
        selenium exceptions on failures
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-quic")
    options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")
    options.add_argument("--log-level=3")
    options.add_argument(f"--window-size={window_size}")

    # Tell Chrome to accept insecure/self-signed certs
    options.set_capability("acceptInsecureCerts", True)

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return driver.page_source

    except WebDriverException:
        # on any rendering failure, fallback to static fetch
        try:
            return fetch_static_html(url, timeout=timeout)
        finally:
            driver.quit()

    finally:
        driver.quit()
