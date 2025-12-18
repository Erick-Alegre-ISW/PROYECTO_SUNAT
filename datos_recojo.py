import re
from typing import Dict, Any, List


def parse_declaracion(ruta_archivo: str) -> Dict[str, Any]:
    datos: Dict[str, Any] = {
        "DETRACCION": 0,
        "RUC": None,
        "ESTABLECIMIENTO": None,
        "ITEMS": [],
        "TIPO_OPERACION": None,
        "CODIGO_DETRACCION": None,
        "CTA_BANCO": None,
        "PORCENTAJE_DETRACCION": 0.0,
        "MONTO_DETRACCION": 0.0,
        "ORIGEN_UBICACION": {},
        "DESTINO_UBICACION": {},
        "REGISTRO_MTC": None,
        "CONFIGURACION_VEHICULAR": None,
        "CARGA_UTIL": 0.0,
        "VALOR_REFERENCIAL": 0.0
    }

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas: List[str] = [line.strip() for line in f.readlines()]

    i = 0
    precios: List[float] = []

    while i < len(lineas):
        linea = lineas[i]

        if linea.startswith("RUC:"):
            datos["RUC"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("INDIQUE EL ESTABLECIMIENTO"):
            datos["ESTABLECIMIENTO"] = linea.split(":", 1)[1].strip()

        # --- AQUÍ ESTABA EL ERROR DEL RESUMEN, ESTE ES EL BUCLE COMPLETO ---
        elif linea.startswith("ITEMS"):
            i += 1
            while i < len(lineas) and lineas[i].startswith("ORIGEN:"):
                partes = [p.strip() for p in lineas[i].split("|")]
                item = {}
                for p in partes:
                    llave, valor = p.split(":", 1)
                    llave = llave.strip().lower()
                    valor = valor.strip()
                    if llave == "precio":
                        precio = float(valor)
                        item["precio"] = precio
                        precios.append(precio)
                    else:
                        key_map = {
                            "origen": "origen", "destino": "destino",
                            "trasportista": "transportista", "remitente": "remitente"
                        }
                        item[key_map.get(llave, llave)] = valor
                datos["ITEMS"].append(item)
                i += 1
            continue
        # -------------------------------------------------------------------

        elif linea.startswith("TIPO DE OPERACION:"):
            datos["TIPO_OPERACION"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("CODIGO DETRACCION:"):
            datos["CODIGO_DETRACCION"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("CTA BANCO NACION:"):
            datos["CTA_BANCO"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("PORCENTAJE DETRACCION:"):
            datos["PORCENTAJE_DETRACCION"] = float(linea.split(":", 1)[1].strip())
        elif linea.startswith("ORIGEN DEPARTAMENTO:"):
            datos["ORIGEN_UBICACION"]["departamento"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("ORIGEN PROVINCIA:"):
            datos["ORIGEN_UBICACION"]["provincia"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("ORIGEN DISTRITO:"):
            datos["ORIGEN_UBICACION"]["distrito"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("ORIGEN DIRECCION:"):
            datos["ORIGEN_UBICACION"]["direccion"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("DESTINO DEPARTAMENTO:"):
            datos["DESTINO_UBICACION"]["departamento"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("DESTINO PROVINCIA:"):
            datos["DESTINO_UBICACION"]["provincia"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("DESTINO DISTRITO:"):
            datos["DESTINO_UBICACION"]["distrito"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("DISTRITO DIRECCION:") or linea.startswith("DESTINO DIRECCION:"):
            datos["DESTINO_UBICACION"]["direccion"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("REGISTRO MTC:"):
            datos["REGISTRO_MTC"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("CONFIGURACION VEHICULAR:"):
            datos["CONFIGURACION_VEHICULAR"] = linea.split(":", 1)[1].strip()
        elif linea.startswith("CARGA UTIL:"):
            datos["CARGA_UTIL"] = float(linea.split(":", 1)[1].strip())

        i += 1

    # Cálculos
    total_venta = sum(precios) * 1.18
    datos["VALOR_REFERENCIAL"] = total_venta

    if total_venta >= 700:
        datos["DETRACCION"] = 1
        porcentaje = datos["PORCENTAJE_DETRACCION"] if datos["PORCENTAJE_DETRACCION"] else 4.0
        datos["MONTO_DETRACCION"] = total_venta * porcentaje / 100
    else:
        datos["DETRACCION"] = 0
        datos["MONTO_DETRACCION"] = 0.0

    return datos