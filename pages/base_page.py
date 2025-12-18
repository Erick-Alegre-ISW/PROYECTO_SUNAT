from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import Tuple
import time


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def espera(self, locator: Tuple[str, str], timeout: int = 10):
        """Espera explicita para elementos clickeables."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def switch_to_frame_with_element(self, locator: Tuple[str, str], timeout: int = 10) -> bool:
        """La lógica robusta de iframes que arreglamos antes."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                for iframe in iframes:
                    self.driver.switch_to.default_content()
                    try:
                        self.driver.switch_to.frame(iframe)
                        if self.driver.find_elements(*locator):
                            return True
                    except:
                        continue
                self.driver.switch_to.default_content()
                time.sleep(0.5)
            except Exception:
                time.sleep(0.5)

        self.driver.switch_to.default_content()
        raise Exception(f"No se encontró el elemento {locator} tras {timeout}s")

    def volver_contenido_principal(self):
        self.driver.switch_to.default_content()