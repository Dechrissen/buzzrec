# Recommender Ideas

- Content-based filtering recommendation engine
- Will ultimately be a Python package hosted on PyPI
- User will enter config settings in `config.txt` (email address to email, frequency to email, etc.) and 'taste' settings in `settings.txt`  to initialize the similarity matrix
- User should start by populating the empty file `settings.txt` to specify two things:
  - keywords interested in
  - keywords to avoid (?)
- If there is nothing in the file upon starting the engine, it will notify the user to do so before starting


## Scraping LingBuzz

- Homepage is organized into a table, with each row (paper) comprised of 4 cells:
  - authors || newness of upload || format type / link to paper || title / link to abstract


## To Do

- Write function that collects papers from LingBuzz according to user-defined pos/neg keywords to get user-specific training data (abstracts)
- Write function that does a search query on LingBuzz for each user-entered keyword in `config.json` and adds those papers to the initial training csv dataset
