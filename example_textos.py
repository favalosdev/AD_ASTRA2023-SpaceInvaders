from textos import NEWSProcessor;
import numpy as np
import sys
import json
import dill
import re
import unicodedata
import nltk
import pandas as pd
nltk.download('stopwords')
from nltk.corpus import stopwords
from stanza.pipeline.processor import Processor, register_processor
import stanza
stanza.download('es')
from num2words import num2words
from langdetect import detect
nltk.download('stopwords')


news = NEWSProcessor()

news.ner_from_url("https://www.elespectador.com/ambiente/amazonas/el-aumento-de-la-mineria-ilegal-amenaza-a-un-pueblo-del-amazonas-en-aislamiento/", "hola.json")
