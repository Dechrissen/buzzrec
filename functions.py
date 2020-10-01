import random
import requests
from bs4 import BeautifulSoup
#import tensorflow

class Paper():
    def __init__(self, title, authors, abstract, keywords):
        assert type(title) is str
        assert type(authors) is list
        for author in authors:
            assert type(author) is str
        assert type(abstract) is str
        assert type(keywords) is list
        for keyword in keywords:
            assert type(keyword) is str
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.keywords = keywords

def scrape():
    """Scrapes LingBuzz for new papers to extract title, authors, abstract, and keywords. Creates a new Paper object."""

    # Get LingBuzz homepage
    webpage = requests.get('https://ling.auf.net/lingbuzz')
    return

def classifier(text):
    """Returns a (random) binary classification value for a given text.

    Parameters
    ----------
        text : the text to be classified

    Returns
    -------
        bool
    """
    return random.choice([True, False])

def train(model):
    """Trains a neural network classifier."""
    return
