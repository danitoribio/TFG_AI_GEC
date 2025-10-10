def calcular_media(archivo):
    try:
        with open(archivo, 'r') as f:
            # Leer todas las líneas del archivo y eliminar posibles espacios en blanco
            lineas = f.readlines()
            numeros = [float(linea.strip()) for linea in lineas if linea.strip()]

        if len(numeros) == 0:
            print("El archivo está vacío o contiene solo líneas en blanco.")
            return None
        
        # Calcular la media
        media = sum(numeros) / len(numeros)
        return media
        
    except FileNotFoundError:
        print(f"El archivo {archivo} no fue encontrado.")
        return None
    except ValueError as e:
        print(f"Error de conversión: {e}")
        return None

# Usa la función
import os
import glob

# Ruta a la carpeta que contiene los archivos .txt
carpeta_txt = "llama_tuned"

# Lista para almacenar los nombres de archivo
archivos_txt = []

# Obtener todos los archivos .txt de la carpeta
for archivo in glob.glob(os.path.join(carpeta_txt, "*.txt")):
    archivos_txt.append(os.path.basename(archivo))
for archivo_txt in archivos_txt:
    archivo_txt = carpeta_txt + "/" + archivo_txt
    media = calcular_media(archivo_txt)
    if media is not None:
        print(f"{archivo_txt}: {media}")
        print()