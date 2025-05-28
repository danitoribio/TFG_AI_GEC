import streamlit as st
import ollama
from ollama import chat
from ollama import ChatResponse
from difflib import Differ

# Diccionario de textos por idioma
translations = {
    'en': {
        'title': 'Text Corrector',
        'input_label': 'Write your text here:',
        'button_label': 'Perform Correction',
        'error_message': 'Please enter a text to perform the correction.',
        'original_text': 'Original Text',
        'corrected_text': 'Corrected Text',
    },
    'es': {
        'title': 'Corrector de texto',
        'input_label': 'Escribe aquí tu texto:',
        'button_label': 'Realizar corrección',
        'error_message': 'Por favor, introduce un texto para realizar la corrección.',
        'original_text': 'Texto Original',
        'corrected_text': 'Texto Corregido',
    }
}

# Selector de idioma
language = st.selectbox("Select Language / Selecciona Idioma:", options=['en', 'es'])

# Textos en el idioma seleccionado
text = translations[language]

# Función para resaltar cambios
def highlight_changes(original, corrected):
    differ = Differ()
    changes = list(differ.compare(original.split(), corrected.split()))
    result_html = []

    for word in changes:
        if word.startswith('-'):
            result_html.append(f'<span style="color: red; text-decoration: line-through;">{word[2:]}</span>')
        elif word.startswith('+'):
            result_html.append(f'<span style="color: green;">{word[2:]}</span>')
        elif word.startswith(' '):
            result_html.append(word[2:])

    return ' '.join(result_html)

# Interfaz de la aplicación Streamlit
st.title(text['title'])

# Crear un cuadro de texto para la entrada
user_input = st.text_area(text['input_label'], "")

# Botón de predicción
if st.button(text['button_label']):
    if user_input:
        response: ChatResponse = chat(model='LlamaGEC:latest', messages=[
                    {
            'role': 'user',
            'content': user_input,
                    },
                ])
        resultado = response['message']['content']
        col1, col2 = st.columns(2)
        with col1:
            st.header(text['original_text'])
            st.write(user_input)
        with col2:
            st.header(text['corrected_text'])
            highlighted_html = highlight_changes(user_input, resultado)
            st.markdown(highlighted_html, unsafe_allow_html=True)
    else:
        st.error(text['error_message'])