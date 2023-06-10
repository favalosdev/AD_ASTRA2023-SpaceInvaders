from textos.news import ner_from_url, ner_from_file, ner_from_str
from textos.text_preprocessor import textPreprocessor

ner_from_url("https://cnnespanol.cnn.com/2023/06/10/wilson-perro-ninos-desaparecidos-colombia-orix/", "sad.json")