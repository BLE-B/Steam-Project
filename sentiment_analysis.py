import json
import pandas as pd
import nltk
import re
import spacy
from matplotlib import pyplot as plt
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split


nlp = spacy.load('en_core_web_sm')
stopwords = spacy.lang.en.stop_words.STOP_WORDS
ct_vectorizer = CountVectorizer(lowercase=True,
                                strip_accents='ascii',
                                ngram_range=(1, 2), 
                                stop_words=['english', 'german'])
tf_vectorizer = TfidfVectorizer()

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def get_df(json_file = 'players_with_bio.json'):
    with open(json_file, 'r') as f:
        data = json.load(f)
        players_df = pd.DataFrame.from_dict(data)
    return players_df
    
def tokenize(df):
    word_count = []
    for content in df['bio']:
        match_digits_and_words = ('(\d+|\w+)')
        gna1 = re.findall(match_digits_and_words, content)
        gna2 = word_tokenize(content)
        gna3 = re.match('[a-z0-9 ]+', content) # whole sentences until comma
        #print(gna3)
        word_count.append(len(content))
    print(word_count)
    print(len(word_count))
    plt.hist(word_count)

def tokenize2(string):
    doc = nlp(string)
    tokens = [token.text for token in doc]
    print(tokens)
    return tokens
    
def lemmatize(string):
    doc = nlp(string)
    lemmas = [token.lemma_ for token in doc]
    print(lemmas)
    return lemmas

def word_count(string):
    words = string.split()
    return len(words)

def remove_stop_words(string):
    doc = nlp(string)
    lemmas = [token.lemma_ for token in doc]
    a_lemmas = [lemma for lemma in lemmas 
            if lemma.isalpha() and lemma not in stopwords]
    print(' '.join(a_lemmas))
    return ' '.join(a_lemmas)

def pos_tagging(string):
    doc = nlp(string)
    pos = [(token.text, token.pos_) for token in doc]
    print(pos)
    return pos

def entity_tagging(string):
    doc = nlp(string)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def vectorize(df, col, vectorizer):
    series = df[col]
    bow_matrix = vectorizer.fit_transform(series)
    print(bow_matrix.toarray())
    print(bow_matrix.shape)
    return pd.DataFrame(bow_matrix.toarray())

def sentiment_analyze(df, X, y):
    X_train, X_test, y_train, y_test = train_test_split(df[X],
                                                        df[y],
                                                        test_size=.25,
                                                        random_state=12345,
                                                        stratify=df[y])
    X_train_bow = vectorizer.fit_transform(X_train)
    X_test_bow = vectorizer.transform(X_test)
    clf = MultinomialNB()
    clf.fit(X_train_bow, y_train)
    accuracy = clf.score(X_test_bow, y_test)
    print('acc: ', accuracy)


def apply_func(players_df, new_col, used_col, func):
    players_df[new_col] = players_df[used_col].apply(func)



if __name__ == '__main__':        
    players_df = get_df()
    tokenize(players_df)
    vectorized_df = vectorize(players_df, 'bio', ct_vectorizer)
    #sentiment_analyze(players_df, 'bio', label)