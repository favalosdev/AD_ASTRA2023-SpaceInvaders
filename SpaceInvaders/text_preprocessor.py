from sklearn.base import BaseEstimator, TransformerMixin
import re
import unicodedata
import nltk
import pandas as pd
from nltk.corpus import stopwords
import stanza
stanza.download('es')
from num2words import num2words
nltk.download('stopwords')

class textPreprocessor(BaseEstimator, TransformerMixin):
  def __init__(self):
      print('pipe')
      
  def replace_numbers(self, words):
    """Reemplaza todas las apariciones de enteros en una lista de palabras tokenizadas con representación textual.
    
    Args: 
      words (list): Lista de palabras tokenizadas.

    Returns:
      list: Lista de palabras de enteros reemplazadas por su representación textual.
    """
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = num2words(word, lang='es')
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words
  
  def remove_nonlatin(self, words):
      """Elimina caracteres non-Latin desde una lista de palabras tokenizadas.
          
      Args:
        words (list): Lista de palabras tokenizadas.
              
      Returns:
        list: Lista de palabras sin los caracteres non-Latin.
      """
      new_words = []
      for word in words:
          new_word = ''
          for ch in word:
              if unicodedata.name(ch).startswith(('LATIN', 'DIGIT', 'SPACE')):
                  new_word += ch
          new_words.append(new_word)
      return new_words
  
  def remove_stopwords(self, words):
      """Elimina las palabras vacías (stopwords) desde una lista de palabras tokenizadas.
        
        Args:
            words (list): Lista de palabras tokenizadas.
            
        Returns:
            list: Lista de palabras sin las palabras vacías.
      """
      new_words = []
      stop_words = set(stopwords.words('spanish'))
      s = set(stopwords.words('spanish'))
      for word in words:
          if word not in s:
              new_words.append(word)
      return new_words
  
  def remove_punctuation(self, words):
    """Elimina signos de puntuación de una lista de palabras tokenizadas.

        Args:
            words (list): Lista de palabras tokenizadas.
            
        Returns:
            str: Una cadena de caracteres sin signos de puntuación.
    """
    new_words = ''
    for word in words:
            new_words += re.sub(r'[^\w\s]', ' ', word)
    return new_words
  
  def tokenLemma(self, X):
    """ Aplica la tokenización, lematización, etiquetado de partes del discurso y tokenización de palabras compuestas utilizando Stanza.
        
      Args:
        X (pd.Series): Datos de entrada que contienen texto.
            
      Returns:
        list: Lista de objetos de Documento de Stanza.
    """
    nlp = stanza.Pipeline('es', processors='tokenize,mwt,pos,lemma', use_gpu=False)

    X = X.apply(self.remove_punctuation)
    
    in_docs = [stanza.Document([], text=d) for d in X]
    return nlp(in_docs)
  
  def procesamientoPalabras(self, words):
    """ Realiza tareas de procesamiento de palabras, incluyendo la eliminación de caracteres no latinos, reemplazo de números
    y eliminación de palabras vacías en una lista de palabras tokenizadas.
        
    Args:
      words (list): Lista de palabras tokenizadas.
            
    Returns:
      list: Lista de palabras procesadas.
    """
    words = self.remove_nonlatin(words)
    words = self.replace_numbers(words)
    words = self.remove_stopwords(words)
    return words
  
  def transform(self, X):
    """
    Aplica el pipeline de preprocesamiento de texto para transformar los datos de entrada.
    
    Args:
        X (pd.Series): Datos de entrada que contienen texto.
        
    Returns:
        pd.Series: Datos transformados.
    """
    out_docs = self.tokenLemma(X)
    palabras = []
    for doc in out_docs:
      reviewAct = []
      for sentence in doc.sentences:
        for word in sentence.words:
          if(word.pos != 'PUNCT' and word.pos != 'SYM'):
            reviewAct.append(word.lemma.lower())
      palabras.append(reviewAct)
    X = pd.Series(palabras)
    X = X.apply(self.procesamientoPalabras)
    X = X.apply(lambda x: ' '.join(map(str, x)))
    return X
  
  def fit(self, X, y=None):
      """
      Ajusta el preprocesador de texto a los datos de entrada.
    
    Args:
        X (arreglo o matriz dispersa): Datos de entrada en los que ajustar el preprocesador.
        y (arreglo, opcional): Etiquetas de destino. Por defecto es None.
        
    Returns:
        self
      """
      return self