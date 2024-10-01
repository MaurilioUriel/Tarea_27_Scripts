import subprocess
import re

# Lista de puertos estándar
standard_ports = {22, 25, 80, 465, 587, 8080}

def is_suspicious_connection(line):
    # Expresión regular para capturar líneas de netstat
    match = re.search(r'\s(\d+)\s', line)
    if match:
        port = int(match.group(1))
        return port not in standard_ports
    return False

def main():
    try:
        # Ejecutar el script de Bash
        result = subprocess.run(['./monitoreo_red.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Almacenar las conexiones sospechosas
        suspicious_connections = []

        # Analizar la salida
        for line in result.stdout.splitlines():
            if 'ESTABLISHED' in line and is_suspicious_connection(line):
                suspicious_connections.append(line)

        # Generar el reporte
        if suspicious_connections:
            with open('reporte_conexiones_sospechosas.txt', 'w') as report_file:
                report_file.write("Conexiones sospechosas identificadas:\n")
                for conn in suspicious_connections:
                    report_file.write(conn + '\n')
            print("Reporte generado: reporte_conexiones_sospechosas.txt")
        else:
            print("No se encontraron conexiones sospechosas.")

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el script de Bash: {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()