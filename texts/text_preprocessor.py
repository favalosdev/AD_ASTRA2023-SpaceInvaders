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
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = num2words(word, lang='es')
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words
  
  def remove_nonlatin(self, words):
      new_words = []
      for word in words:
          new_word = ''
          for ch in word:
              if unicodedata.name(ch).startswith(('LATIN', 'DIGIT', 'SPACE')):
                  new_word += ch
          new_words.append(new_word)
      return new_words
  
  def remove_stopwords(self, words):
      """Remove stop words from list of tokenized words"""
      new_words = []
      stop_words = set(stopwords.words('spanish'))
      s = set(stopwords.words('spanish'))
      for word in words:
          if word not in s:
              new_words.append(word)
      return new_words
  
  def remove_punctuation(self, words):
    """Remove punctuation from list of tokenized words"""
    new_words = ''
    for word in words:
            new_words += re.sub(r'[^\w\s]', ' ', word)
    return new_words
  
  def tokenLemma(self, X):
    nlp = stanza.Pipeline('es', processors='tokenize,mwt,pos,lemma', use_gpu=False)

    X = X.apply(self.remove_punctuation)
    
    in_docs = [stanza.Document([], text=d) for d in X]
    return nlp(in_docs)
  
  def procesamientoPalabras(self, words):
    words = self.remove_nonlatin(words)
    words = self.replace_numbers(words)
    words = self.remove_stopwords(words)
    return words
  
  def transform(self, X):
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
      return self