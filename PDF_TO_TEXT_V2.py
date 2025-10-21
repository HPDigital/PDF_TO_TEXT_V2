"""
PDF_TO_TEXT_V2
"""

#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[2]:


import openai
from PyPDF2 import PdfReader
import re
from dotenv import load_dotenv
import os
import pdfplumber

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la API de OpenAI a partir de la variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

# Función para traducir texto usando la API de OpenAI (versión >= 1.0.0)
def traducir_con_openai(texto, modelo="gpt-4"):
    """
    Traduce el texto de inglés a español usando la API de OpenAI.

    Args:
        texto (str): Texto en inglés a traducir.
        modelo (str): Modelo de OpenAI a utilizar para la traducción. Por defecto "gpt-4".

    Returns:
        str: Texto traducido o None si ocurre un error.
    """
    mensajes = [
        {"role": "system", "content": "Eres un asistente de traducción de inglés a español."},
        {"role": "user", "content": f"Traduce el siguiente texto de inglés a español:\n\n{texto}"}
    ]

    try:
        respuesta = openai.chat.completions.create(  # Cambia a la nueva llamada a la API
            model=modelo,
            messages=mensajes,
            max_tokens=2048,
            temperature=0.3
        )
        return respuesta.choices[0].message.content  # Acceder a la respuesta correctamente
    except Exception as e:
        print(f"Error en la traducción: {e}")
        return None
#print(completion.choices[0].message)
# Función para extraer texto de un archivo PDF
# def extraer_texto_pdf(pdf_path):
#     """
#     Extrae el texto de todas las páginas de un archivo PDF.

#     Args:
#         pdf_path (str): Ruta del archivo PDF.

#     Returns:
#         str: Todo el texto extraído del PDF.
#     """
#     reader = PdfReader(pdf_path)
#     all_text = ""

#     for page_num, page in enumerate(reader.pages):
#         print(f"Extrayendo texto de la página {page_num + 1}...")
#         all_text += page.extract_text()

#     return all_text




def extraer_texto_pdf(pdf_path):
    """
    Extrae el texto de todas las páginas de un archivo PDF, ignorando cuadros y gráficos.

    Args:
        pdf_path (str): Ruta del archivo PDF.

    Returns:
        str: Todo el texto extraído del PDF.
    """
    all_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"Extrayendo texto de la página {page_num + 1}...")
            # Extraer solo el texto, omitiendo elementos gráficos
            page_text = page.extract_text()
            if page_text:
                all_text += page_text

    return all_text


# Función para dividir el texto en secciones basadas en frases
def dividir_texto_por_frases(texto, seccion_size=1500):
    """
    Divide el texto en secciones sin cortar oraciones.

    Args:
        texto (str): Texto a dividir.
        seccion_size (int): Tamaño máximo de cada sección. Por defecto 1500 caracteres.

    Returns:
        list: Lista de secciones del texto.
    """
    oraciones = re.split(r'(?<=[.!?]) +', texto)  # Dividir por fin de oración
    secciones = []
    actual_seccion = ""

    for oracion in oraciones:
        if len(actual_seccion) + len(oracion) <= seccion_size:
            actual_seccion += oracion + " "
        else:
            secciones.append(actual_seccion.strip())
            actual_seccion = oracion + " "

    if actual_seccion:
        secciones.append(actual_seccion.strip())

    return secciones

# Función principal para traducir el PDF y guardar el resultado en un archivo de texto
def traducir_y_guardar_pdf(pdf_path, output_txt_path, seccion_size=1500):
    """
    Traduce un archivo PDF por secciones y guarda el resultado en un archivo de texto.

    Args:
        pdf_path (str): Ruta del archivo PDF a traducir.
        output_txt_path (str): Ruta donde se guardará el archivo de salida.
        seccion_size (int): Tamaño máximo de cada sección a traducir. Por defecto 1500 caracteres.
    """
    # Extraer texto del PDF
    all_text = extraer_texto_pdf(pdf_path)

    # Dividir el texto en secciones
    secciones = dividir_texto_por_frases(all_text, seccion_size)

    # Traducir y guardar cada sección
    with open(output_txt_path, "w", encoding="utf-8") as text_file:
        for idx, seccion in enumerate(secciones):
            print(f"Traduciendo sección {idx + 1} de {len(secciones)}...")
            traduccion = traducir_con_openai(seccion)
            if traduccion:
                text_file.write(traduccion + "\n\n")
                print(f"Sección {idx + 1} traducida y guardada.")
            else:
                print(f"Error en la sección {idx + 1}, omitiendo...")

    print(f"Traducción completa. El archivo traducido está en {output_txt_path}")

# Ejecutar el script
if __name__ == "__main__":
    pdf_path = r"C:\Users\HP\Downloads\Market-ResearchinPractice_AnIntroductiontoGainingGreaterMarketInsight.pdf"  # Ruta a tu archivo PDF
    output_txt_path = r"C:\Users\HP\Downloads\Market-ResearchinPractice_AnIntroductiontoGainingGreaterMarketInsight.txt"  # Ruta donde se guardará el archivo traducido
    traducir_y_guardar_pdf(pdf_path, output_txt_path)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


import openai
import re
import os
import pdfplumber
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la API de OpenAI a partir de la variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

def traducir_con_openai(texto, modelo="gpt-4"):
    """
    Traduce el texto de inglés a español usando la API de OpenAI.

    Args:
        texto (str): Texto en inglés a traducir.
        modelo (str): Modelo de OpenAI a utilizar para la traducción. Por defecto "gpt-4".

    Returns:
        str: Texto traducido o None si ocurre un error.
    """
    try:
        respuesta = openai.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un asistente de traducción de inglés a español."},
                {"role": "user", "content": f"Traduce el siguiente texto de inglés a español:\n\n{texto}"}
            ],
            max_tokens=2048,
            temperature=0.3
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        print(f"Error en la traducción: {e}")
        return None

def extraer_texto_pdf(pdf_path):
    """
    Extrae el texto de todas las páginas de un archivo PDF, ignorando cuadros y gráficos.

    Args:
        pdf_path (str): Ruta del archivo PDF.

    Returns:
        str: Todo el texto extraído del PDF.
    """
    texto_completo = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                print(f"Extrayendo texto de la página {page_num + 1}...")
                page_text = page.extract_text()
                if page_text:
                    texto_completo += page_text
    except Exception as e:
        print(f"Error al extraer texto del PDF: {e}")
    return texto_completo

def dividir_texto_por_frases(texto, seccion_size=1500):
    """
    Divide el texto en secciones sin cortar oraciones.

    Args:
        texto (str): Texto a dividir.
        seccion_size (int): Tamaño máximo de cada sección. Por defecto 1500 caracteres.

    Returns:
        list: Lista de secciones del texto.
    """
    oraciones = re.split(r'(?<=[.!?]) +', texto)
    secciones, actual_seccion = [], ""

    for oracion in oraciones:
        if len(actual_seccion) + len(oracion) <= seccion_size:
            actual_seccion += oracion + " "
        else:
            secciones.append(actual_seccion.strip())
            actual_seccion = oracion + " "

    if actual_seccion:
        secciones.append(actual_seccion.strip())

    return secciones

def traducir_y_guardar_pdf(pdf_path, output_txt_path, seccion_size=1500):
    """
    Traduce un archivo PDF por secciones y guarda el resultado en un archivo de texto.

    Args:
        pdf_path (str): Ruta del archivo PDF a traducir.
        output_txt_path (str): Ruta donde se guardará el archivo de salida.
        seccion_size (int): Tamaño máximo de cada sección a traducir.
    """
    # Extraer y validar texto del PDF
    texto = extraer_texto_pdf(pdf_path)
    if not texto.strip():
        print("No se pudo extraer texto del PDF o el archivo está vacío.")
        return

    # Dividir el texto en secciones
    secciones = dividir_texto_por_frases(texto, seccion_size)

    # Traducir y guardar cada sección
    try:
        with open(output_txt_path, "w", encoding="utf-8") as archivo_salida:
            for idx, seccion in enumerate(secciones):
                print(f"Traduciendo sección {idx + 1} de {len(secciones)}...")
                traduccion = traducir_con_openai(seccion)
                if traduccion:
                    archivo_salida.write(traduccion + "\n\n")
                    print(f"Sección {idx + 1} traducida y guardada.")
                else:
                    print(f"Error en la sección {idx + 1}, omitiendo...")
        print(f"Traducción completa. El archivo traducido está en {output_txt_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

# Ejecutar el script
if __name__ == "__main__":
    pdf_path = r"C:\Users\HP\Downloads\Market-ResearchinPractice_AnIntroductiontoGainingGreaterMarketInsight.pdf"
    output_txt_path = r"C:\Users\HP\Downloads\Market-ResearchinPractice_AnIntroductiontoGainingGreaterMarketInsight.txt"
    traducir_y_guardar_pdf(pdf_path, output_txt_path)


# In[ ]:





# In[ ]:




