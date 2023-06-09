# -*- coding: utf-8 -*-
from flair.data import Sentence
from flair.models import SequenceTagger
import json
import pandas as pd
import requests
from flair.data import Sentence
from newspaper import Article
import dill

filename_svm = './textos/pipeline.joblib' # Ubicación del archivo entregado
# Deserializar el objeto del archivo
with open(filename_svm, 'rb') as f:
    svm = dill.load(f)
    

class NEWSProcessor:
    def __init__(self):
        self.tagger = SequenceTagger.load("flair/ner-spanish-large")

    def ner_from_str(self, text, output_path):
        """
        Realiza el procesamiento NER (Reconocimiento de Entidades Nombradas) en un texto.

        Args:
            text (str): El texto de entrada.
            output_path (str): La ruta del archivo de salida donde se guardará el resultado en formato JSON.

        Returns:
            str: El texto con las etiquetas NER agregadas.
        """
        sentence = Sentence(text)
        self.tagger.predict(sentence)
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

        df2 = {'New': [sentence.text]}
        df2 = pd.DataFrame(df2)
        response['impact'] = svm.predict(df2)[0]
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False)
        return sentence.to_tagged_string()

    def ner_from_file(self, text_path, output_path):
        """
        Realiza el procesamiento NER en un archivo de texto.

        Args:
            text_path (str): La ruta del archivo de texto de entrada.
            output_path (str): La ruta del archivo de salida donde se guardará el resultado en formato JSON.

        Returns:
            str: El texto con las etiquetas NER agregadas.
        """
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return self.ner_from_str(text, output_path)



    def ner_from_url(self, url, output_path):
        """
        Realiza el procesamiento NER en el contenido de una URL.

        Args:
            url (str): La URL del contenido.
            output_path (str): La ruta del archivo de salida donde se guardará el resultado en formato JSON.

        Returns:
            str: El texto con las etiquetas NER agregadas.
        """
        requests.packages.urllib3.disable_warnings()
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        # parse html content
        response = requests.get(url, headers=headers, verify=False)
        # Download the web page content without SSL certificate verification
        #response = requests.get(url, verify=False)
        response.encoding = 'utf-8'
        # Create an Article object
        toi_article = Article(url, language="es")

        # Set the HTML content of the article
        #toi_article.set_html(response.text)
        toi_article.download(input_html=response.content)
        # Parse the article
        toi_article.parse()

        # Perform natural language processing
        #toi_article.nlp()

        # Extract title

        text = toi_article.text
        return self.ner_from_str(text, output_path)
