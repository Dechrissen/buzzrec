## Ideas

- Python package hosted on PyPI
- If there is nothing in the file upon starting the engine, it will notify the user to do so before starting
- buzzrec will run (and recommend papers) as often as you run it. This can be made easier with a cronjob on Linux


## Scraping LingBuzz

- Homepage is organized into a table, with each row (paper) comprised of 4 cells:
  - authors || newness of upload || format type / link to paper || title / link to abstract


## To Do

- This paper: 'How obligatory irrelevance, symmetric alternatives, and dense scales conspire: The case of modified numerals and ignorance' has <em> tags in the abstract on LingBuzz. For this reason, it doesn't parse well and I had to skip it if scrapeLingBuzzHomePage sees it. Fix this so it can be used normally.
- Add evaluation metric for the tool. Maybe some kind trial period with actual users who give feedback on their experience
- determine what threshold for similarity is considered recommendation-worthy
- more carefully construct the user model (via explicit binary feedback, etc.)
- implement the email digest system