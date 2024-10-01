#!/bin/bash

# Función para verificar el código de retorno
check_returncode() {
    if [ $? -ne 0 ]; then
        echo "Error: Falló la ejecución del comando."
        exit 1
    fi
}

# Intervalo de actualización en segundos
while true; do
    clear
    echo "Conexiones de red activas (ESTABLISHED):"
    
    netstat -tunapl | grep ESTABLISHED
    check_returncode  # Verifica el código de retorno del comando netstat

done