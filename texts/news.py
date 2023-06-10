from flair.data import Sentence
from flair.models import SequenceTagger
import json
import requests
from newspaper import Article
import pandas as pd
from sklearn.pipeline import Pipeline
import joblib
import numpy as np
import docx
from PyPDF2 import PdfReader
import pkg_resources
import regex as re



def getTextWord(filename: str) -> str:
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def getText(text_path: str) -> str:
    text = ''
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def getTextPdf(text_path: str) -> str:
    temp = open(text_path, 'rb')
    pdf_reader = PdfReader(temp)
    num_pages = len(pdf_reader.pages)
    full_text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        full_text += text
    return full_text


def load_model() -> Pipeline:
    stream = pkg_resources.resource_stream(__name__, 'pipeline.joblib')
    model = joblib.load(stream)
    return model


def ner_from_str(text: str, output_path: str):
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
    response['dates'] = re.findall('(19[89][0-9]|20[0-4][0-9]|2050)', text) + re.findall('([a-zA-Z]+) del (\d{4})', text)
    new = {'New': [sentence.text]}
    new = pd.DataFrame(new)
    model = load_model().predict_proba(new)
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
    save_json(response, output_path)


def ner_from_file(text_path: str, output_path: str):
    if text_path.endswith('.pdf'):
        text = getTextPdf(text_path)
    elif text_path.endswith('.docx'):
        text = getTextWord(text_path)
    else:
        text = getText(text_path)
    ner_from_str(text, output_path)


def ner_from_url(url: str, output_path: str):

    requests.packages.urllib3.disable_warnings()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    response = requests.get(url, headers=headers, verify=False)
    response.encoding = 'utf-8'
    toi_article = Article(url, language="es")
    toi_article.download(input_html=response.content)
    toi_article.parse()

    text = toi_article.text
    ner_from_str(text, output_path)


def save_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
