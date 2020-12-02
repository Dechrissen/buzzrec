import pandas as pd
#import numpy as np
from rake_nltk import Rake
import json
import csv
from functions import *

def create_csv():
    """Creates an initial user-specific dataset (`dataset.csv`) of papers from
    LingBuzz according to keywords in `config.json`.
    """
    # open config file to get user-entered parameters
    f = open('config.json', 'r')
    obj = f.read()
    config = json.loads(obj)
    f.close()

    # find papers from LingBuzz matching user preferences
    collected_papers = []
    for term in config['keywords']:
        papers_to_add = queryLingBuzz(term)
        collected_papers.extend(papers_to_add)

    # create csv dataset file with relevant papers
    with open('dataset.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['Title', 'Link', 'Authors', 'Abstract', 'Keywords', 'Date'])
        for paper in collected_papers:
            # Catch potential UnicodeEncodeError (certain characters don't want to be written in csv files)
            try:
                filewriter.writerow([paper.title, paper.link, paper.authors, paper.abstract, paper.keywords, paper.date])
            except UnicodeEncodeError:
                print('UnicodeEncodeError: \'' + paper.title[:31]+'...\'', 'skipped')
                continue



def create_df():
    df = pd.read_csv('dataset.csv', sep=',', encoding='ISO-8859-1')
    df = df[['Title', 'Link', 'Authors', 'Abstract', 'Keywords', 'Date']]
    return df


# Tests
#create_csv()
df = create_df()
df['Key_words'] = ''
for index, row in df.iterrows():
    abstract = row['Abstract']
    r = Rake()
    r.extract_keywords_from_text(abstract)
    keywords_dict_scores = dict(r.get_word_degrees())
    df.at[index, 'Key_words'] = list(keywords_dict_scores.keys())
#print(df['Title'][6])
#print(df['Key_words'][6])
#df.drop(columns = ['Abstract'], inplace = True)
print(df.head(3))
