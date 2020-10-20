import random
import requests
from bs4 import BeautifulSoup, NavigableString
#import tensorflow as tf

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

def scrapeLingBuzz():
    """Scrapes LingBuzz homepage for new papers to extract title, authors, abstract, and keywords. Creates a new Paper object for each new upload."""

    # Get LingBuzz homepage
    homepage = requests.get('https://ling.auf.net/lingbuzz')
    soup = BeautifulSoup(homepage.content, 'html.parser')
    # Sequentially work down to the table that stores first page of papers
    html = list(soup.children)[1]
    body = list(html.children)[1]
    main_table = list(body.children)[2]
    tbody = list(main_table.children)[0]
    tr = list(tbody.children)[0]
    td_1 = list(tr.children)[0]

    # Store html table of entire first page of papers in recent_papers_table
    # Each element in this list is of class 'bs4.element.Tag'
    # Each element (paper) is a <tr>
    # Each <tr> is comprised of 4 <td> tags containing: Authors, Newness, PDF link, Title
    recent_papers_table = list(td_1.children)

    # Authors
    authors_td = list(list(recent_papers_table[20].children)[0].children)
    for tag in authors_td:
        if tag.name == 'a':
            print(tag.get_text())

    # Newness
    newness_td = list(list(recent_papers_table[20].children)[1].children)[0]
    if isinstance(newness_td, NavigableString):
        print("none here") # eventually ignore this entry if there are no children (i.e. a singular <b>)
    else:
        print(list(newness_td.children)[0])

    # PDF link
    pdf_td = list(list(recent_papers_table[1].children)[2].children)[0]
    pdf_link = pdf_td['href']
    print(pdf_link)


def classifier(text):
    """Returns a (random for now) binary classification value for a given text.

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

# tests
scrapeLingBuzz()
