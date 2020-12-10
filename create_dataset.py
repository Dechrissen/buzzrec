import pandas as pd
import numpy as np
from rake_nltk import Rake
import json
import ast
import csv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from functions import *


def clean_authors(author_list):
    return [author.lower().strip().replace(' ', '').replace(',', '') for author in author_list]

def create_csv():
    """Creates an initial user-specific dataset (`user.csv`) of papers from
    LingBuzz according to keywords in `config.json`.
    """
    print("Fetching papers ... this may take a few minutes.")
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
    print("Creating initial dataset in user.csv ...")
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
    print("Extracting keywords from papers ...")
    # create new column which relevant columns (Authors, Abstract, Keywords) will be collapsed into
    df['bag_of_words'] = ''

    for index, row in df.iterrows():
        # create empty list to which final key words are added per paper
        bag_of_words_list = []
        # collect Authors column
        authors = row['Authors']
        author_list = ast.literal_eval(authors)
        # clean each author in the author list
        author_list = clean_authors(author_list)
        # add authors to bag_of_words_list
        bag_of_words_list.extend(author_list)

        # collect Abstract column
        abstract = row['Abstract']
        # first extract keywords from Abstract column via nltk's Rake
        r = Rake()
        r.extract_keywords_from_text(abstract)
        keywords_dict_scores = dict(r.get_word_degrees())
        abstract_keywords = list(keywords_dict_scores.keys())
        # add abstract_keywords to bag_of_words_list
        bag_of_words_list.extend(abstract_keywords)

        # collect Keywords column
        keywords = row['Keywords']
        keywords_list = ast.literal_eval(keywords)
        # add keywords to bag_of_words_list
        bag_of_words_list.extend(keywords_list)

        words = ''
        for word in bag_of_words_list:
            words = words + word
        # add everything to bag_of_words column for current paper
        df.at[index, 'bag_of_words'] = words

    # drop columns
    df.drop(columns = ['Authors', 'Abstract', 'Keywords'], inplace=True)

    return df








# Tests
np.set_printoptions(formatter={'float': lambda x: "{0:0.8f}".format(x)})

#create_csv()

# create the dataframe
df = create_df()

# merge the dataframe's columns into one bag_of_words column
df = merge_df(df)

# set the dataframe's Title column as index
df.set_index('Title', inplace=True)
#print(df.head())

# Actual stuff

# instantiating and generating the count matrix
#count = CountVectorizer()
#count_matrix = count.fit_transform(df['bag_of_words'])

# instantiating and generating the tfidf matrix
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['bag_of_words'])

# create series for indexes
indices = pd.Series(df.index)
print(indices[:5])

# create series for PDF links
lnx = pd.Series(df['Link'])


# generating the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

#new one from tdidf article
#cosine_sim = linear_kernel(count_matrix, count_matrix)
print(cosine_sim)

# save the matrix as CSV
#np.savetxt('similarity_matrix.csv', cosine_sim, delimiter=',')



def recommendations(title, cosine_sim):
    """Function that takes in paper title as input and returns the top 5 recommended papers."""

    recommended_papers = []

    # getting the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    print(type(score_series))
    print(len(score_series))


    # getting the indexes of the 5 most similar papers
    top_5_indexes = list(score_series.iloc[1:11].index)
    print(score_series.iloc[1:11].index)
    print(score_series.iloc[1:11])


    # populating the list with the titles of the best 5 matching papers
    for i in top_5_indexes:
        recommended_papers.append(list(df.index)[i] + " " + df['Link'][i])

    return recommended_papers

title = 'Exploring sound symbolic knowledge of English speakers using Pokemon character names'
recs = recommendations(title, cosine_sim)
for r in recs:
    print(r)
