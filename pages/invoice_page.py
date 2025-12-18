from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from pages.base_page import BasePage
from typing import Dict, Any, List
import time
import random


class SunatInvoicePage(BasePage):
    # --- LOCATORS (Copiados de tu versión funcional) ---
    _MENU_EMPRESAS = (By.XPATH, "//div[@id='divOpcionServicio2']")
    _MENU_FACTURA = (By.XPATH, "//a[div[contains(., 'Emisión de Factura Electrónica')]]")

    _RADIO_DETRACCION_SI = (By.XPATH, "//input[@id='inicio.detraccion.subTipoDetraccion01']")
    _RADIO_DETRACCION_NO = (By.XPATH, "//input[@id='inicio.detraccion.subTipoDetraccion00']")
    _POPUP_ACEPTAR = (By.XPATH, "//span[@id='dlgBtnAceptar_label']/ancestor::span[@role='button']")

    _INPUT_RUC = (By.XPATH, "//input[@id='inicio.numeroDocumento']")

    _RADIO_ESTAB_SI = (By.XPATH, "//input[@id='inicio.subTipoEstEmi01']")
    _RADIO_ESTAB_NO = (By.XPATH, "//input[@id='inicio.subTipoEstEmi00']")
    _BTN_CONTINUAR = (By.XPATH, '//*[@id="inicio.botonGrabarDocumento"]')

    # Items
    _BTN_ADD_ITEM = (By.XPATH, '//*[@id="factura.addItemButton"]')
    _RADIO_SERVICIO = (By.XPATH, "//input[@id='item.subTipoTI02']")
    _INPUT_DESC = (By.NAME, "descripcion")
    _INPUT_PRECIO = (By.ID, "item.precioUnitario")
    _BTN_ACEPTAR_ITEM = (By.ID, "item.botonAceptar")
    _BTN_GRABAR_ITEMS = (By.XPATH, '//*[@id="factura.botonGrabarDocumento"]')

    # Docs y Detracción
    _BTN_DOCS = (By.XPATH, '//*[@id="docsrel.botonOtrosDocsRelacionados"]')
    _INPUT_TIPO_DOC = (By.XPATH, '//*[@id="docrel.tipoDocumento"]')
    _INPUT_SERIE = (By.ID, "docrel.serieDocumento")
    _INPUT_NUMERO = (By.ID, "docrel.numeroDocumentoInicial")
    _BTN_ADD_DOC = (By.ID, "docrel.botonAddDoc")
    _BTN_ACEPTAR_DOCS = (By.ID, "docrel.botonAceptar")

    _BTN_INFO_DET = (By.XPATH, '//*[@id="docsrel.botonInformacionDetraccion"]')
    _INPUT_TIPO_OP = (By.XPATH, '//*[@id="infDetraccion.detraccionTipoOperacion"]')
    _INPUT_COD_BIEN = (By.XPATH, '//*[@id="infDetraccion.detraccionCodBien"]')
    _INPUT_CTA = (By.ID, "infDetraccion.detraccionNroCtaBco")
    _INPUT_MEDIO = (By.ID, "infDetraccion.detraccionMedioPago")
    _INPUT_TASA = (By.XPATH, '//*[@id="infDetraccion.detraccionTasa"]')
    _INPUT_MONTO = (By.ID, "infDetraccion.detraccionMonto")

    _BTN_UBIGEO_ORI = (By.ID, "infDetraccion.agregarUbigeoOrigen")
    _BTN_UBIGEO_DEST = (By.ID, "infDetraccion.agregarUbigeoDestino")
    _INPUT_ORI_DEP = (By.XPATH, '//*[@id="detraccionOrigen.emisorDpto"]')
    _INPUT_DEST_DEP = (By.XPATH, '//*[@id="detraccionDestino.emisorDpto"]')

    _INPUT_MTC = (By.XPATH, '//*[@id="infDetraccion.registroMTC"]')
    _BTN_ACEPTAR_DET = (By.ID, "infDetraccion.botonAceptar")

    _BTN_EMITIR_FINAL = (By.XPATH, '//*[@id="docsrel.botonGrabarDocumento"]')

    def navegar_a_emision(self):
        print("[NAV] Navegando a menú de facturación...")
        self.espera(self._MENU_EMPRESAS).click()
        self.espera(self._MENU_FACTURA).click()
        print("[INFO] Esperando carga de applet Java...")
        time.sleep(4)  # Pausa vital restaurada

    def configurar_cabecera(self, ruc_receptor: str, tiene_detraccion: int, establecimiento: str):
        print("[FACTURA] Configurando cabecera...")

        # 1. Detracción
        locator_detraccion = self._RADIO_DETRACCION_SI if tiene_detraccion == 1 else self._RADIO_DETRACCION_NO
        self.switch_to_frame_with_element(locator_detraccion)
        self.espera(locator_detraccion).click()

        if tiene_detraccion == 1:
            self.espera(self._POPUP_ACEPTAR).click()
            time.sleep(1.5)  # Pausa por popup

        self.volver_contenido_principal()

        # 2. RUC
        self.switch_to_frame_with_element(self._INPUT_RUC)
        elm_ruc = self.espera(self._INPUT_RUC)
        elm_ruc.send_keys(ruc_receptor)
        elm_ruc.send_keys(Keys.TAB)
        time.sleep(1)  # Pausa para carga de Razón Social
        self.volver_contenido_principal()

        # 3. Establecimiento
        ESTAB = str(int(float(establecimiento)))
        locator_estab = self._RADIO_ESTAB_SI if ESTAB == "1" else self._RADIO_ESTAB_NO
        self.switch_to_frame_with_element(locator_estab)
        self.espera(locator_estab).click()

        # 4. Continuar
        self.espera(self._BTN_CONTINUAR).click()
        self.volver_contenido_principal()
        time.sleep(2)  # Pausa de transición de pantalla

    def agregar_items(self, items: List[Dict[str, Any]]):
        print(f"[FACTURA] Procesando {len(items)} items...")

        for item in items:
            self.switch_to_frame_with_element(self._BTN_ADD_ITEM)
            self.espera(self._BTN_ADD_ITEM).click()
            self.volver_contenido_principal()

            time.sleep(0.5)

            self.switch_to_frame_with_element(self._RADIO_SERVICIO)
            self.espera(self._RADIO_SERVICIO).click()

            # Llenado
            self.driver.find_element(*self._INPUT_DESC).send_keys(
                f"TRANSPORTE DE {item['origen']} A {item['destino']} | GUIA TRANSPORTISTA 0001-{item['transportista']} | GUIA REMITENTE {item['remitente']}"
            )
            self.driver.find_element(*self._INPUT_PRECIO).clear()
            self.driver.find_element(*self._INPUT_PRECIO).send_keys(f"{item['precio']:.2f}")

            self.driver.find_element(*self._BTN_ACEPTAR_ITEM).click()
            self.volver_contenido_principal()
            time.sleep(0.5)  # Pequeña pausa entre items

        # Grabar para pasar a la sig pantalla
        self.switch_to_frame_with_element(self._BTN_GRABAR_ITEMS)
        self.driver.find_element(*self._BTN_GRABAR_ITEMS).click()
        self.volver_contenido_principal()
        time.sleep(2)  # Pausa de transición

    def agregar_guias(self, items: List[Dict[str, Any]]):
        print("[FACTURA] Agregando guías...")
        self.switch_to_frame_with_element(self._BTN_DOCS)
        self.driver.find_element(*self._BTN_DOCS).click()
        self.volver_contenido_principal()

        # Pausa para que el modal aparezca completamente
        time.sleep(1)

        self.switch_to_frame_with_element(self._INPUT_TIPO_DOC)
        elm_tipo = self.espera(self._INPUT_TIPO_DOC)
        elm_tipo.send_keys("GUIA DE REMISION TRANSPORTISTA")
        elm_tipo.send_keys(Keys.TAB)  # Importante para cerrar sugerencias

        for item in items:
            # 1. Aseguramos estar en el iframe y que el campo SERIE sea visible
            self.switch_to_frame_with_element(self._INPUT_SERIE)

            # 2. SERIE: Limpiamos y escribimos
            elm_serie = self.driver.find_element(*self._INPUT_SERIE)
            elm_serie.clear()
            elm_serie.send_keys("0001")

            # 3. NÚMERO: Limpiamos y escribimos
            elm_numero = self.driver.find_element(*self._INPUT_NUMERO)
            elm_numero.clear()
            elm_numero.send_keys(str(item['transportista']))

            # 4. Click en AGREGAR
            self.driver.find_element(*self._BTN_ADD_DOC).click()

            # 5. FRENADO: Esperamos a que SUNAT agregue la fila a la tabla visualmente
            # Sin esto, el loop intenta escribir el siguiente antes de que el servidor responda
            time.sleep(0.5)

            # 6. Reset del contexto para la siguiente vuelta
            self.volver_contenido_principal()

        # Al terminar el loop, aceptamos todo el modal
        print("[FACTURA] Finalizando carga de guías...")

        # A veces el botón Aceptar tarda en activarse si acabas de agregar un ítem
        time.sleep(0.5)

        # Volvemos a buscar el iframe porque salimos en el loop
        self.switch_to_frame_with_element(self._BTN_ACEPTAR_DOCS)
        self.driver.find_element(*self._BTN_ACEPTAR_DOCS).click()
        self.volver_contenido_principal()

        time.sleep(1)  # Pausa de seguridad al cerrar el modal

    def llenar_detraccion(self, datos: Dict[str, Any]):
        if datos["DETRACCION"] != 1:
            return

        print("[FACTURA] Llenando detalle de detracción...")
        self.switch_to_frame_with_element(self._BTN_INFO_DET)
        self.driver.find_element(*self._BTN_INFO_DET).click()
        self.volver_contenido_principal()

        # Datos Generales
        self.switch_to_frame_with_element(self._INPUT_TIPO_OP)
        self.espera(self._INPUT_TIPO_OP).send_keys(datos["TIPO_OPERACION"])
        self.volver_contenido_principal()

        self.switch_to_frame_with_element(self._INPUT_COD_BIEN)
        self.driver.find_element(*self._INPUT_COD_BIEN).send_keys(datos["CODIGO_DETRACCION"])
        self.volver_contenido_principal()

        self.switch_to_frame_with_element(self._INPUT_CTA)
        self.driver.find_element(*self._INPUT_CTA).send_keys(datos["CTA_BANCO"])
        self.driver.find_element(*self._INPUT_MEDIO).send_keys("001-Depósito en cuenta")
        self.volver_contenido_principal()

        self.switch_to_frame_with_element(self._INPUT_TASA)
        self.driver.find_element(*self._INPUT_TASA).send_keys(f"{datos['PORCENTAJE_DETRACCION']:.2f}")
        self.driver.find_element(*self._INPUT_MONTO).send_keys(f"{datos['MONTO_DETRACCION']:.1f}0")

        # Origen
        self.driver.find_element(*self._BTN_UBIGEO_ORI).click()
        self.volver_contenido_principal()

        time.sleep(0.5)

        self.switch_to_frame_with_element(self._INPUT_ORI_DEP)
        self.espera(self._INPUT_ORI_DEP).send_keys(datos["ORIGEN_UBICACION"]["departamento"])
        self.driver.find_element(By.ID, "detraccionOrigen.emisorProv").send_keys(datos["ORIGEN_UBICACION"]["provincia"])
        self.driver.find_element(By.ID, "detraccionOrigen.emisorDist").send_keys(datos["ORIGEN_UBICACION"]["distrito"])
        self.driver.find_element(By.ID, "detraccionOrigen.direccion").send_keys(datos["ORIGEN_UBICACION"]["direccion"])
        self.driver.find_element(By.ID, "detraccionOrigen.botonAceptarUbigeo").click()
        self.volver_contenido_principal()

        # Destino
        self.switch_to_frame_with_element(self._BTN_UBIGEO_DEST)
        self.driver.find_element(*self._BTN_UBIGEO_DEST).click()
        self.volver_contenido_principal()

        time.sleep(0.5)

        self.switch_to_frame_with_element(self._INPUT_DEST_DEP)
        self.espera(self._INPUT_DEST_DEP).send_keys(datos["DESTINO_UBICACION"]["departamento"])
        self.driver.find_element(By.ID, "detraccionDestino.emisorProv").send_keys(
            datos["DESTINO_UBICACION"]["provincia"])
        self.driver.find_element(By.ID, "detraccionDestino.emisorDist").send_keys(
            datos["DESTINO_UBICACION"]["distrito"])
        self.driver.find_element(By.ID, "detraccionDestino.direccion").send_keys(
            datos["DESTINO_UBICACION"]["direccion"])
        self.driver.find_element(By.ID, "detraccionDestino.botonAceptarUbigeo").click()
        self.volver_contenido_principal()

        time.sleep(0.5)

        # Finales
        self.switch_to_frame_with_element(self._INPUT_MTC)
        self.driver.find_element(*self._INPUT_MTC).send_keys(datos["REGISTRO_MTC"])
        self.driver.find_element(By.ID, "infDetraccion.confVehicular").send_keys(datos["CONFIGURACION_VEHICULAR"])
        self.driver.find_element(By.ID, "infDetraccion.CargaUtil").send_keys(f"{datos['CARGA_UTIL']:.2f}")
        self.driver.find_element(By.ID, "infDetraccion.valServTransporte").send_keys(
            f"{datos['VALOR_REFERENCIAL']:.2f}")
        self.driver.find_element(*self._BTN_ACEPTAR_DET).click()
        self.volver_contenido_principal()

    def emitir_factura(self):
        print("[FACTURA] Emitiendo factura final...")
        self.switch_to_frame_with_element(self._BTN_EMITIR_FINAL)
        self.espera(self._BTN_EMITIR_FINAL).click()
        self.volver_contenido_principal()