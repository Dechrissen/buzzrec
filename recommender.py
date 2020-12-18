from functions import *
from create_dataset import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np


def recommend(title, cosine_sim):
    """Function that takes paper title as input and returns the top 5 recommended papers."""

    recommended_papers = {}

    # getting the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    #print(type(score_series))
    #print(len(score_series))

    # getting the indexes of the 5 most similar papers
    top_5_indexes = list(score_series.iloc[1:5].index)
    highest_score = float(score_series.iloc[1])
    #print(score_series.iloc[1:5].index)
    #print(score_series.iloc[1:5])

    # populating the list with the titles of the best 5 matching papers
    for i in top_5_indexes:
        recommended_papers[list(df.index)[i]] = df['Link'][i]

    return recommended_papers, highest_score

#####################################
######## Program begins here ########
#####################################
np.set_printoptions(formatter={'float': lambda x: "{0:0.8f}".format(x)})

# construct a .csv file containing all papers found on LingBuzz from querying
# with user-entered keywords

#create_csv()

# create a copy of `user.csv` with 5 extra papers appended
test_titles = create_csv_copy('user.csv')

# create the dataframe according to `user.csv`
df = create_df()

# merge the dataframe's columns (authors, abstract, keywords) into
# one bag_of_words column
df = merge_df(df)
print('sample cell:', df['bag_of_words'][3])

# set the dataframe's Title column as index
df.set_index('Title', inplace=True)
#print(df.head())

# instantiate and generate the count matrix
#count = CountVectorizer()
#count_matrix = count.fit_transform(df['bag_of_words'])

# instantiate and generate the TF-IDF matrix
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['bag_of_words'])

# create series for indexes
indices = pd.Series(df.index)
#print(indices[:5])

# create series for PDF links
lnx = pd.Series(df['Link'])

# generate the cosine similarity matrix from the TF-IDF matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
#print(cosine_sim)

# save the matrix into .csv
np.savetxt('similarity_matrix.csv', cosine_sim, delimiter=',')

# Reading the .csv into an array (for later use)
#cosine_sim = np.genfromtxt("similarity_matrix.csv", delimiter=",")


highest = 0
recommendation = None
for t in test_titles:
    recs, score = recommend(t, cosine_sim)
    if score > highest:
        highest = score
        recommendation = t
print('Recommendation:', recommendation, '\nLink to PDF:', df['Link'][recommendation])


#title = 'A wug-shaped curve in sound symbolism: The case of Japanese Pokémon names'

#for r in recs.keys():
    #print(r)
    #print(recs[r])
