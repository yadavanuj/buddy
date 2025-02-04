import re
import nltk
nltk.download('punkt_tab')
nltk.download("wordnet")
from nltk.corpus import wordnet

'''
Steps:
Tokenize identifiers (split camelCase, snake_case).
Normalize (lowercase, remove special chars).
Expand abbreviations (cust → customer, info → information).
Use NLP for Synonyms (fetch → get, client → customer).
'''

def split_identifier(identifier):
    words = re.findall(r'[A-Za-z][a-z]*|[A-Z][a-z]*|[0-9]+', identifier)
    return [w.lower() for w in words]

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

name = "getCustomerData"
words = split_identifier(name)
synonyms = {w: get_synonyms(w) for w in words}

print("Split words:", words)
print("Synonyms:", synonyms)
