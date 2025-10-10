from ollama import chat
from ollama import ChatResponse
import warnings
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import json

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    
    # Configuración del argumento de entrada
    parser = argparse.ArgumentParser(description="Procesamiento de texto con LlamaGEC.")
    parser.add_argument("--output", type=str, default="llama-tuned.json", help="Archivo de salida JSON")
    args = parser.parse_args()
    
    # Obtener el archivo de salida
    file_out = args.output
    
    # Cargar el dataset
    data = pd.read_csv("dataset.csv", quotechar='"')
    
    # Dividir el dataset en train y test
    train_df, test_df = train_test_split(data, test_size=0.2, random_state=42)
    print(len(test_df))
    
    # Lista para almacenar los resultados
    resultados = []
    i = 0
    # Iterar sobre cada fila de test_df
    for index, row in test_df.iterrows():
        # Saltar la primera iteración si deseas omitir la primera fila de datos
        if index == 0:
            continue
        
        input_text = row['input']
        target = row['target']
       
        # Obtener la respuesta del modelo
        response: ChatResponse = chat(model='LlamaGEC:latest', messages=[
            {
                'role': 'user',
                'content': input_text,
            },
        ])
        
        # Obtener el contenido de la respuesta
        corrected_text = response['message']['content']
        
        # Agregar el resultado a la lista
        resultados.append({
            'input': input_text,
            'correction': corrected_text,
            'target': target
        })
        i+=1
        if i % 5 == 0:
            print(f'Progresso:{i/690}')
    
    # Escribir todos los resultados en el archivo JSON
    with open(file_out, 'w', encoding='utf-8') as json_file:
        json.dump(resultados, json_file, ensure_ascii=False, indent=4)
    
    print(f'Resultados guardados en {file_out}')