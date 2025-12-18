from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SunatLoginPage(BasePage):
    # Locators internos
    _RUC = (By.ID, "txtRuc")
    _USUARIO = (By.ID, "txtUsuario")
    _CLAVE = (By.ID, "txtContrasena")
    _BTN_LOGIN = (By.ID, "btnAceptar")

    def cargar_portal(self):
        self.driver.get("https://e-menu.sunat.gob.pe/cl-ti-itmenu/MenuInternet.htm?pestana=*&agrupacion=*")

    def iniciar_sesion(self, ruc: str, usuario: str, clave: str):
        print(f"[LOGIN] Iniciando sesión con RUC {ruc}...")
        self.espera(self._RUC).send_keys(ruc)
        self.driver.find_element(*self._USUARIO).send_keys(usuario)
        self.driver.find_element(*self._CLAVE).send_keys(clave)
        self.driver.find_element(*self._BTN_LOGIN).click()