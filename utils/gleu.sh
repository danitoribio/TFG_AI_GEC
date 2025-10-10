#!/bin/bash

# Ruta a la carpeta que contiene los archivos JSON
json_folder="llama_tuned"

# Procesar cada archivo JSON en la carpeta
for json_file in "$json_folder"/*.json; do
  # Comprobar si el archivo JSON existe y es un archivo regular
  if [[ -f "$json_file" ]]; then
    echo "Procesando archivo: $json_file"

    # Número de observaciones
    num_observations=$(jq length "$json_file")

    # Iterar sobre cada observación en el archivo JSON
    for i in $(seq 0 $(($num_observations - 1))); do
      # Leer los campos de la observación actual
      reference=$(jq -r ".[$i].target" "$json_file")
      original=$(jq -r ".[$i].input" "$json_file")
      output=$(jq -r ".[$i].correction" "$json_file")

      echo "Observación: $i"
      # Crear los archivos correspondientes
      echo "$reference" > reference.txt
      echo "$original" > original.txt
      echo "$output" > output.txt

      # Ejecutar el script de Python
      python compute_gleu.py -r reference.txt -s original.txt -o output.txt -f "$json_file".txt
    done
  else
    echo "No se encontró el archivo o no es un archivo regular: $json_file"
  fi
done