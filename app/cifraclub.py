"""Extract a Cifra Club chart using a remote browser."""

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected

CIFRACLUB_URL = "https://www.cifraclub.com.br/"

class CifraClub():
    """CifraClub Class"""
    def __init__(self):
        options = Options()
        options.add_argument('-headless')
        options.page_load_strategy = 'eager'
        self.driver = webdriver.Remote(
            os.getenv('SELENIUM_URL', 'http://selenium:4444/wd/hub'),
            options=options,
        )
        self.driver.set_page_load_timeout(25)

    def cifra(self, artist: str, song: str) -> dict:
        """Lê a página HTML e extrai a cifra e meta dados da música."""
        url = f"{CIFRACLUB_URL}{artist}/{song}/"
        result = {'cifraclub_url': url}
        try:
            self.driver.get(url)
            content = WebDriverWait(self.driver, 20).until(
                expected.presence_of_element_located((By.CSS_SELECTOR, '[data-chord-content]'))
            )
            title = self.driver.title.replace(' - Cifra Club', '')
            name, separator, performer = title.partition(' - ')
            tone = self.driver.find_elements(By.CSS_SELECTOR, '[data-chord-config] button')
            result.update({
                'name': name.strip(),
                'artist': performer.strip() if separator else '',
                'tone': tone[0].text.strip() if tone else '',
                'cifra': content.get_attribute('innerText').splitlines(),
            })
        except Exception as error: # pylint: disable=broad-except
            result['error'] = 'Não foi possível extrair esta cifra.'
            result['detail'] = type(error).__name__
        finally:
            self.driver.quit()

        return result
