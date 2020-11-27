import random
import requests
from bs4 import BeautifulSoup, NavigableString
import re
#import tensorflow as tf

class Paper():
    def __init__(self, title, link, authors, abstract, keywords, date):
        assert type(title) is str
        assert type(link) is str
        assert type(authors) is list
        for author in authors:
            assert type(author) is str
        assert type(abstract) is str
        assert type(keywords) is list
        for keyword in keywords:
            assert type(keyword) is str
        assert type(date) is str
        self.title = title
        self.link = link
        self.authors = authors
        self.abstract = abstract
        self.keywords = keywords
        self.date = date

def scrapeLingBuzzHomePage():
    """Scrapes LingBuzz homepage for new papers to extract title, link to paper,
     authors, abstract, and keywords. Creates a new Paper object for each new
     upload."""

    # Get LingBuzz homepage
    homepage = requests.get('https://ling.auf.net/lingbuzz/')
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
    n = 24 # number of the paper to find
    # Authors
    authors = []
    authors_td = list(list(recent_papers_table[n].children)[0].children)
    for tag in authors_td:
        if tag.name == 'a':
            authors.append(tag.get_text())

    # Newness / year
    newness_td = list(list(recent_papers_table[n].children)[1].children)[0]
    if isinstance(newness_td, NavigableString):
        date = str(newness_td)
    else:
        date = str(list(newness_td.children)[0])
    date = date.split('-')[0]

    # PDF link
    pdf_td = list(list(recent_papers_table[n].children)[2].children)[0]
    pdf_link = 'https://ling.auf.net' + pdf_td['href']

    # Link to summary
    summary_td = list(list(recent_papers_table[n].children)[3].children)[0]
    summary_link = 'https://ling.auf.net' + summary_td['href']

    # Title
    title = summary_td.get_text()

    # Abstract
    # Use summary link to get a paper's page
    page = requests.get(summary_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Sequentially work down to the paper's abstract
    html = list(soup.children)[1]
    body = list(html.children)[1]
    # The abstract is at the 5th index of the body's children list
    abstract = str(list(body.children)[5])

    # Keywords
    keywords_tr = list(list(body.children)[6].children)[3]
    keywords_list_td = list(keywords_tr.children)[1]
    keywords = keywords_list_td.get_text()
    keywords = re.split(r'[,|;]', keywords)
    keywords = [k.strip() for k in keywords]

    # Construct Paper object
    current_paper = Paper(title, pdf_link, authors, abstract, keywords, date)
    return current_paper

def queryLingBuzz(query):
    """Takes a query and returns a list of Paper objects resulting from that
    query on LingBuzz.

    Parameters
    ----------
    query : string
        The string to query LingBuzz with.

    Returns
    -------
    list
        List of Paper objects.

    """
    # Get LingBuzz search results page according to `query`
    page = requests.get(f'https://ling.auf.net/lingbuzz/_search?q={query}')
    soup = BeautifulSoup(page.content, 'html.parser')
    # Sequentially work down to the table that stores first page of papers
    html = list(soup.children)[1]
    body = list(html.children)[1]
    main_table = list(body.children)[0]

    # Check if query returned 'nothing found' and return empty list if so
    if str(list(list(main_table.children)[0].children)[0]) == 'nothing found':
        print('results: nothing found')
        return []

    # Store html table of entire first page of papers in main_table
    # Each element in this list is of class 'bs4.element.Tag'
    # Each element (paper) is a <tr>
    # Each <tr> is comprised of 4 <td> tags containing: NULL, Authors, Newness, Title (link to summary)

    #n = 3 # number of the paper to find

    collected_papers = []
    # Iterate through table of entire search query results
    for n in range(len(list(main_table))):
        # Authors
        authors = []
        authors_td = list(list(list(main_table.children)[n].children)[0].children)[0]
        for tag in authors_td:
            if tag.name == 'a':
                authors.append(tag.get_text())

        # Year
        date = None
        date_td = list(list(list(main_table.children)[n].children)[0].children)[1]
        if isinstance(date_td, NavigableString):
            pass
        else:
            date = list(date_td.children)[0].strip('(').strip(')')


        # Link to summary
        summary_td = list(list(list(list(main_table.children)[n].children)[0].children)[2].children)[0]
        summary_link = 'https://ling.auf.net' + summary_td['href']

        # Title
        title = summary_td.get_text()


        # Abstract
        # Use summary link to get a paper's page
        page = requests.get(summary_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Sequentially work down to the paper's abstract
        html = list(soup.children)[1]
        body = list(html.children)[1]
        # The abstract is at the 5th index of the body's children list
        abstract = str(list(body.children)[5])

        # PDF link
        # I don't know why I had to add this error catching... certain paper summary pages
        # aren't formatted consistently? The ones from 'semantics archive'
        try:
            pdf_tr = list(list(body.children)[6].children)[0]
        except IndexError:
            continue
        # Catch a potential nonexistent PDF link in summary page (and skip current iteration / paper)
        try:
            link_a = list(list(pdf_tr.children)[1].children)[1]
        except AttributeError:
            continue
        pdf_link = 'https://ling.auf.net' + link_a['href']

        # Keywords
        keywords_tr = list(list(body.children)[6].children)[3]
        keywords_list_td = list(keywords_tr.children)[1]
        keywords = keywords_list_td.get_text()
        keywords = re.split(r'[,|;]', keywords)
        keywords = [k.strip() for k in keywords]

        # Construct Paper object
        current_paper = Paper(title, pdf_link, authors, abstract, keywords, date)
        collected_papers.append(current_paper)

    return collected_papers




def classifier(text):
    """Returns a random (for now) binary classification value for a given text.

    Parameters
    ----------
    text : the text to be classified

    Returns
    -------
    bool
    """
    return random.choice([True, False])


# Tests

#current_paper = scrapeLingBuzzHomePage()

#print(current_paper.title)
#print(current_paper.link)
#print(current_paper.authors)
#print(current_paper.abstract)
#print(current_paper.keywords)
#print(current_paper.date)

#collected_papers = queryLingBuzz('pokemon')
#for x in collected_papers:
    #print(x.date)
