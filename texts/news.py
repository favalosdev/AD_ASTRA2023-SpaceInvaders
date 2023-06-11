import json
import docx
import joblib
import numpy as np
import pandas as pd
import pkg_resources
import regex as re
import requests
from flair.data import Sentence
from flair.models import SequenceTagger
from newspaper import Article
from PyPDF2 import PdfReader
from sklearn.pipeline import Pipeline


def __getTextWord(file_path: str) -> str:
    """
    Obtiene el texto de un documento .docx o un documento de Word.

    Args:
        file_path (str): Ruta del archivo.

    Returns:
        str: Texto extraído del documento.
    """
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def __getText(text_path: str) -> str:
    """
    Obtiene el texto de un documento .txt o un documento de texto.

    Args:
        text_path (str): Ruta del archivo.

    Returns:
        str: Texto extraído del documento.
    """
    text = ''
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def __getTextPdf(text_path: str) -> str:
    """
    Obtiene el texto de un documento .pdf o un documento PDF.

    Args:
        text_path (str): Ruta del archivo.

    Returns:
        str: Texto extraído del documento.
    """
    temp = open(text_path, 'rb')
    pdf_reader = PdfReader(temp)
    num_pages = len(pdf_reader.pages)
    full_text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        full_text += text
    return full_text


def __load_model() -> Pipeline:
    """
    Carga el modelo que se encuentra en el archivo pipeline.joblib.

    Returns:
        Pipeline: Modelo cargado.
    """
    stream = pkg_resources.resource_stream(__name__, 'pipeline.joblib')
    model = joblib.load(stream)
    return model


def ner_from_str(text: str, output_path: str):
    """
    Obtiene el reconocimiento de entidades con nombre (NER) en formato JSON a partir de una cadena de texto.

    Args:
        text (str): Texto del cual se desea obtener el NER y la clasificación.
        output_path (str): Ruta del archivo .json donde se guardará el resultado.
    """
    sentence = Sentence(text)
    tagger = SequenceTagger.load("flair/ner-spanish-large")
    tagger.predict(sentence)
    entities = dict()
    for entity in sentence.get_spans('ner'):
        tag = entity.tag
        text = entity.text
        if tag in entities:
            # Si la llave ya existe, agregamos el valor a la lista existente
            entities[tag].append(text)
        else:
            # Si la llave no existe, creamos una nueva lista con el valor
            entities[tag] = [text]

    response = {}
    response['text'] = sentence.text
    for key in entities:
        entities[key] = list(set(entities[key]))
        response[key.lower()] = entities[key]
    response['dates'] = list(set(re.findall(r'\b(\d{1,2}\s+(?:de\s+)?(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+(?:de\s+)?\d{4}|\d{4})\b', sentence.text, re.IGNORECASE)))
    new = {'New': [sentence.text]}
    new = pd.DataFrame(new)
    model = __load_model().predict_proba(new)
    maximo = model[0].max()
    prob = np.where(model[0] == maximo)[0][0]
    tag = 'NINGUNA'
    if maximo >= 0.78:
        if prob == 0:
            tag = 'CONTAMINACION'
        elif prob == 1:
            tag = 'DEFORESTACION'
        elif prob == 2:
            tag = 'MINERIA'

    response['impact'] = tag
    __save_json(response, output_path)


def ner_from_file(text_path: str, output_path: str):
    """
    Obtiene el reconocimiento de entidades con nombre (NER) en formato JSON a partir de un archivo.
    El archivo puede ser .txt, .pdf o .docx.

    Args:
        text_path (str): Ruta del archivo del cual se desea obtener el NER y la clasificación.
        output_path (str): Ruta del archivo .json donde se guardará el resultado.
    """
    if text_path.endswith('.pdf'):
        text = __getTextPdf(text_path)
    elif text_path.endswith('.docx'):
        text = __getTextWord(text_path)
    else:
        text = __getText(text_path)
    ner_from_str(text, output_path)


def ner_from_url(url: str, output_path: str):
    """
    Obtiene el reconocimiento de entidades con nombre (NER) en formato JSON a partir de un enlace o URL.

    Args:
        url (str): Enlace del cual se desea obtener el NER y la clasificación.
        output_path (str): Ruta del archivo .json donde se guardará el resultado.
    """
    requests.packages.urllib3.disable_warnings()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    response = requests.get(url, headers=headers, verify=False)
    response.encoding = 'utf-8'
    article = Article(url, language="es")
    article.download(input_html=response.content)
    article.parse()

    text = article.text
    ner_from_str(text, output_path)


def __save_json(data: dict, output_path: str):
    """
    Crea, escribe y guarda el archivo .json.

    Args:
        data: Datos que se guardarán en el archivo .json.
        output_path (str): Ruta del archivo .json donde se guardará el resultado.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
