# Usar la API de Have I Been Pwned?
import requests
import json
import logging
import getpass4

# Configuración de headers
headers = {
    'content-type': 'application/json',
    'api-version': '3',
    'User-Agent': 'python'
}

# Solicitar la API key de forma segura
key = getpass4.getpass("Ingrese su API key: ")
headers['hibp-api-key'] = key

# Preguntar correo a revisar
email = input("Ingrese el correo a investigar: ")

# Inicializar el registro de logs
logging.basicConfig(filename='hibpINFO.log', format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)

# Inicializar el archivo de reporte
reporte_file = f'reporte_{email.replace("@", "_").replace(".", "_")}.txt'
with open(reporte_file, 'w') as report_file:
    report_file.write(f"Reporte de filtraciones para el correo: {email}\n\n")

    # Solicitud
    url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false'

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Lanza un error si la respuesta es un código de error

        data = r.json()
        encontrados = len(data)

        if encontrados > 0:
            print("Los sitios en los que se ha filtrado el correo", email, "son:")
            report_file.write("Filtraciones encontradas:\n")
            for filtracion in data:
                info = (f"Nombre: {filtracion['Name']}\n"
                        f"Dominio: {filtracion['Domain']}\n"
                        f"Fecha de registro: {filtracion['BreachDate']}\n"
                        f"Descripción: {filtracion['Description']}\n\n")
                print(info)
                report_file.write(info)
        else:
            print("El correo", email, "no ha sido filtrado")
            report_file.write("No se encontraron filtraciones.\n")

        msg = f"{email} Filtraciones encontradas: {encontrados}"
        logging.info(msg)

    except requests.exceptions.HTTPError as http_err:
        msg = f"Error HTTP: {http_err}"
        logging.error(msg)
        report_file.write("Ocurrió un error al realizar la solicitud.\n")
    except requests.exceptions.RequestException as req_err:
        msg = f"Error de solicitud: {req_err}"
        logging.error(msg)
        report_file.write("Ocurrió un error de solicitud.\n")
    except Exception as e:
        msg = f"Ocurrió un error inesperado: {e}"
        logging.error(msg)
        report_file.write("Ocurrió un error inesperado.\n")
    else:
        print("Solicitado con éxito..")
    finally:
        print("Fin del proceso.")
        report_file.write("\nProceso finalizado.\n")