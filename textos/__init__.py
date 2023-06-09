# -*- coding: utf-8 -*-
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
from .news import NEWSProcessor
