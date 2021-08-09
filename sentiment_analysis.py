import json
import pandas as pd
import nltk
import re
from matplotlib import pyplot as plt
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def tokenize(json_data = 'players_with_bio.json'):
    with open(json_data, 'r') as f:
        data = json.load(f)
        players_df = pd.DataFrame.from_dict(data)
        word_count = []
        for content in players_df['bio']:
            match_digits_and_words = ('(\d+|\w+)')
            gna1 = re.findall(match_digits_and_words, content)
            gna2 = word_tokenize(content)
            gna3 = re.match('[a-z0-9 ]+', content) # whole sentences until comma
            #print(gna3)
            word_count.append(len(content))
        print(word_count)
        print(len(word_count))
        plt.hist(word_count)


if __name__ == '__main__':        
    tokenize()