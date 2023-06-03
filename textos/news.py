# -*- coding: utf-8 -*-
from flair.data import Sentence
from flair.models import SequenceTagger
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from flair.data import Sentence
from flair.models import TextClassifier


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
        new_clf = TextClassifier.load('data_fst/best-model.pt')
        response['impact'] = new_clf.predict(Sentence(sentence.text))
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

    def remove_tags(self, html):
        """
        Elimina las etiquetas HTML de un contenido.

        Args:
            html (str): El contenido HTML.

        Returns:
            str: El contenido sin las etiquetas HTML.
        """
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        # parse html content
        res = requests.get(html, headers=headers, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()
        # return data by retrieving the tag content
        return ' '.join(soup.stripped_strings)

    def ner_from_url(self, url, output_path):
        """
        Realiza el procesamiento NER en el contenido de una URL.

        Args:
            url (str): La URL del contenido.
            output_path (str): La ruta del archivo de salida donde se guardará el resultado en formato JSON.

        Returns:
            str: El texto con las etiquetas NER agregadas.
        """
        text = self.remove_tags(url)
        return self.ner_from_str(text, output_path)
