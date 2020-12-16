class Paper():
    """Class for Paper objects. Stores metadata for a paper."""
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
