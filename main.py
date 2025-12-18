import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Importamos nuestras clases nuevas
from datos_recojo import parse_declaracion
from pages.login_page import SunatLoginPage
from pages.invoice_page import SunatInvoicePage


def main():
    # 1. Configuración
    load_dotenv()
    datos = parse_declaracion("recojo.txt")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    servicio = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servicio, options=options)

    try:
        # 2. Instanciamos las páginas
        login_page = SunatLoginPage(driver)
        invoice_page = SunatInvoicePage(driver)

        # 3. Flujo de Ejecución (Paso a Paso legible)

        # PASO A: Login
        login_page.cargar_portal()
        login_page.iniciar_sesion(
            os.getenv("RUC_EMISOR"),
            os.getenv("SUNAT_USUARIO"),
            os.getenv("SUNAT_CLAVE")
        )

        # PASO B: Navegación
        invoice_page.navegar_a_emision()

        # PASO C: Llenado
        invoice_page.configurar_cabecera(
            ruc_receptor=datos["RUC"],
            tiene_detraccion=datos["DETRACCION"],
            establecimiento=datos["ESTABLECIMIENTO"]
        )

        invoice_page.agregar_items(datos["ITEMS"])

        invoice_page.agregar_guias(datos["ITEMS"])

        if datos["DETRACCION"] == 1:
            invoice_page.llenar_detraccion(datos)

        # PASO D: Fin
        invoice_page.emitir_factura()

        print("¡Automatización completada con éxito!")

    except Exception as e:
        print(f"Ocurrió un error fatal: {e}")
        # Aquí podrías agregar una captura de pantalla:
        # driver.save_screenshot("error.png")

    finally:
        input("Presiona ENTER para cerrar...")
        driver.quit()


if __name__ == "__main__":
    main()