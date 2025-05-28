from ollama import chat
from ollama import ChatResponse
import warnings
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import time

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    
    # Configuración del argumento de entrada
    parser = argparse.ArgumentParser(description="Procesamiento de texto con LlamaGEC.")
    args = parser.parse_args()
    
    # Cargar el dataset
    data = pd.read_csv("dataset.csv", quotechar='"')
    
    # Dividir el dataset en train y test
    train_df, test_df = train_test_split(data, test_size=0.2, random_state=42)
    
    # Lista para almacenar los tiempos de inferencia
    tiempos_inferencia = []
    i = 0
    # Iterar sobre las primeras 5 filas de test_df
    for index, row in test_df.iterrows():
        if i >= 5:  # Solo queremos procesar 5 textos
            break
        
        input_text = row['input']

        start_time = time.time()  # Iniciar tiempo
        response: ChatResponse = chat(model='GemmaGEC:latest', messages=[
            {
                'role': 'user',
                'content': input_text,
            },
        ])
        end_time = time.time()  # Finalizar tiempo
        i+=1
        # Calcular el tiempo de inferencia y agregarlo a la lista
        tiempo_inferencia = end_time - start_time
        tiempos_inferencia.append(tiempo_inferencia)
    
    # Calcular el tiempo medio de inferencia
    tiempo_medio = sum(tiempos_inferencia) / len(tiempos_inferencia)
    
    print(f'Tiempo medio de inferencia: {tiempo_medio:.4f} segundos')