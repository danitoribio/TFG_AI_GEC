import json
import nltk
from nltk.translate.gleu_score import sentence_gleu
import numpy as np
nltk.download('punkt')  # Corrige el nombre del paquete a 'punkt' para la tokenización

def calculate_gleu_score(predictions, references):
    """
    Calcula el GLEU score para un conjunto de predicciones y referencias.
  
    predictions: Lista de predicciones generadas por el modelo.
    references: Lista de referencias reales (esperadas).
    """
    gleu_scores = []
  
    for pred, ref in zip(predictions, references):
        # Tokenizar las frases
        pred_tokens = nltk.word_tokenize(pred.lower()) # Predicción generada
        ref_tokens = nltk.word_tokenize(ref.lower()) # Referencia real
      
        # Calcular el GLEU score para la frase
        gleu = sentence_gleu([ref_tokens], pred_tokens)
        gleu_scores.append(gleu)
  
    # Devolver el promedio del GLEU score
    return np.mean(gleu_scores)

# Leer el archivo JSON
with open("gemma3-tuned.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# Extraer las predicciones y referencias
predictions = [entry['corrected'][0] for entry in data]
references = [entry['target'] for entry in data]

# Calcular y mostrar el GLEU score promedio
print(calculate_gleu_score(predictions, references))