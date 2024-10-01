#Nombres de miembros:
# Maurilio Uriel García Culebro
# Alondra Castillo Gonzalez
# Erandy Yamileth Escaname Balderas

import requests 
import argparse
import logging
import getpass
import json 
import six 
import sys

if __name__ == '__main__':
    if six.PY3:
        def argument():
            parser = argparse.ArgumentParser(description="Verifica filtraciones de un correo en la API Have I Been Pwned")
            parser.add_argument('-e', dest="email", type=str, help='El correo electrónico a investigar', required=True) 
            args = parser.parse_args()
            email_data = args.email 
            return email_data
        try:
            email = argument()
        except:
            sys.exit("Puedes acceder a la ayuda con -h o --help")

        headers = {
            'content-type': 'application/json',
            'api-version': '3',
            'User-Agent': 'python'
        }

        try: 
            key = getpass.getpass('Introduce la api-key: ')
            headers['hibp-api-key'] = key

            # Solicitud.
            url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false'
            r = requests.get(url, headers=headers)
            
            # Devuelve un código de estado HTTP.
            r.raise_for_status()  
            data = r.json()

            encontrados = len(data)
            if encontrados > 0:
                print(f"Los sitios en los que se ha filtrado el correo {email} son:")
            else:
                print(f"El correo {email} no ha sido filtrado.")

            # Se guarda la información en un archivo txt.
            with open('reporteDeFiltraciones.txt', 'a') as file:  
                file.write(f"Los sitios en los que se ha filtrado el correo {email} son:\n")

                for filtracion in data:
                    name = f"Nombre: {filtracion['Name']}\n"
                    domain = f"Dominio: {filtracion['Domain']}\n"
                    description = f"Descripción: {filtracion['Description']}\n"
                    date = f"Fecha en la que se registró la búsqueda en Have I Been Pwned: {filtracion['AddedDate']}\n"

                    file.write(name)
                    file.write(domain)
                    file.write(date)
                    file.write(description)

                    print(name)
                    print(domain)
                    print(date)
                    print(f"{description}\n")

            msg = f"El número de filtraciones para {email} son: {encontrados}."

        except requests.exceptions.HTTPError as http_err:
            msg = f"Ocurrió un error con la respuesta de la API: {http_err}"  # Captura e imprime el error HTTP.
            logging.basicConfig(filename='hibpERROR.log',
                                format="%(asctime)s %(message)s",
                                datefmt="%m/%d/%Y %H:%M:%S",
                                level=logging.ERROR)
            logging.error(msg)
            sys.exit(1)

        except Exception as err:
            msg = f"Ocurrió un error inesperado: {err}"
            logging.basicConfig(filename='hibpERROR.log',
                                format="%(asctime)s %(message)s",
                                datefmt="%m/%d/%Y %H:%M:%S",
                                level=logging.ERROR)
            logging.error(msg)
            sys.exit(1)

        except json.JSONDecodeError:
            msg = ("No se pudo decodificar la respuesta.")

        else:
            logging.basicConfig(filename='hibpINFO.log',
                                format="%(asctime)s %(message)s",
                                datefmt="%m/%d/%Y %I:%M:%S %p",
                                level=logging.INFO)
            logging.info(msg)

        finally:
            print(msg)

    else: 
        print("Se requiere la versión de Python 3.")
