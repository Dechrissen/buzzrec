# Recommender Ideas

- Content-based filtering recommendation engine
- Will ultimately be a Python package hosted on PyPI
- User will enter config settings in `config.txt` (email address to email, frequency to email, etc.) to initialize the similarity matrix
- If there is nothing in the file upon starting the engine, it will notify the user to do so before starting
- buzzrec will run (and recommend papers) as often as you run it. This can be made easier with a cronjob on Linux


## Scraping LingBuzz

- Homepage is organized into a table, with each row (paper) comprised of 4 cells:
  - authors || newness of upload || format type / link to paper || title / link to abstract


## To Do

- Engine recommends papers from the *same* dataset. Now make it do so for *new* papers collected from LingBuzz via `scrapeLingBuzzHomePage`.
