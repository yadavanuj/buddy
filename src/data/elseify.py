import re
import nltk
nltk.download('punkt_tab')
nltk.download("wordnet")
from nltk.corpus import wordnet

def split_identifier(identifier):
    words = re.findall(r'[A-Za-z][a-z]*|[A-Z][a-z]*|[0-9]+', identifier)
    return [w.lower() for w in words]

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)
