import pandas as pd
#import numpy as np
from rake_nltk import Rake
import json
import csv
from functions import *


def clean_authors(author_list):
    return [author.lower().strip().replace(' ', '') for author in author_list]

def create_csv():
    """Creates an initial user-specific dataset (`user.csv`) of papers from
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
    with open('user.csv', 'w') as csvfile:
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
    """Returns a pandas dataframe object created accoring to `user.csv`."""
    # encoding='ISO-8859-1' is used here to prevent UnicodeDecodeError
    df = pd.read_csv('user.csv', sep=',', encoding='ISO-8859-1')
    df = df[['Title', 'Link', 'Authors', 'Abstract', 'Keywords', 'Date']]
    return df

def merge_df(df):
    """Merges columns in a dataframe of LingBuzz papers into one bag_of_words
    column. The resulting dataframe is organized into two columns : (Title | bag_of_words).

    Parameters
    ----------
    df : dataframe to be merged by column into one bag_of_words column
    """
    bag_of_words_list = []
    # create new column which relevant columns (Authors, Abstract, Keywords) will be collapsed into
    df['bag_of_words'] = ''

    # collect Authors column
    for index, row in df.iterrows():
        authors = row['Authors']

        author_list = json.loads(authors) # TODO fix this, not working for no reason wtf

        # clean each author in the author list
        author_list = clean_authors(author_list)
        # add authors to bag_of_words_list
        bag_of_words_list.extend(author_list)
        # drop Authors column
        df.drop(['Authors'], axis = 1)

    # collect Abstract column
    for index, row in df.iterrows():
        abstract = row['Abstract']
        # first extract keywords from Abstract column via nltk's Rake
        r = Rake()
        r.extract_keywords_from_text(abstract)
        keywords_dict_scores = dict(r.get_word_degrees())
        abstract_keywords = list(keywords_dict_scores.keys())
        # add abstract_keywords to bag_of_words_list
        bag_of_words_list.extend(abstract_keywords)
        # drop Abstract column
        df.drop(['Abstract'], axis = 1)

    # collect Keywords column
    for index, row in df.iterrows():
        keywords = row['Keywords']
        # add keywords to bag_of_words_list
        bag_of_words_list.extend(list(keywords))
        # drop Keywords column
        df.drop(['Keywords'], axis = 1)

    # add everything
    df.at[index, 'bag_of_words'] = bag_of_words_list



# Tests
#create_csv()

# create the dataframe
df = create_df()

# merge the dataframe's columns into one bag_of_words column
merge_df(df)

#print(df['Title'][6])
#print(df['Key_words'][6])
#
print(df.head(3))
