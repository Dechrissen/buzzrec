# buzzrec
A content-based filtering recommendation engine for academic papers in linguistics from [LingBuzz](https://ling.auf.net/lingbuzz).  

`buzzrec` can be downloaded and used locally as a command-line tool.

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)

## Requirements

- Python 3
- numpy==1.19.2
- rake_nltk==1.0.4
- pandas==1.1.4
- requests==2.24.0
- nltk==3.5
- beautifulsoup4==4.9.3
- scikit_learn==0.23.2

## Installation

First, download this repository with the green Code button, or via `git` like below:
```
$ git clone https://github.com/Dechrissen/buzzrec.git
```
Next, install project dependencies. `cd` to the `buzzrec` directory, then:
```
$ pip install -r requirements.txt
```

## Usage

### Initial setup
Populate `config.json` with the following information:
- `keywords`: keywords that define your interests  

For example:
```json
{
  "keywords" : ["computational phonology", "context free grammars", "french vowels"]
}
```

*A note on keywords*: Try to make your keywords more specific than 'phonology' or 'syntax', otherwise the initial data collection will take a while. Each keyword will make a new query to  LingBuzz; the narrower the term, the more specific the results.

### Using the tool

To run the tool, `cd` to the `buzzrec` directory, then:

```
$ python recommender.py
```

The 10 most recent LingBuzz paper uploads will be compared against your specific tastes, and the most similar paper will be recommended to you along with a link to its PDF. You will also see a new file `user.csv` in the project directory. This acts as your user model.

### Starting over (deleting a user model)

To have `buzzrec` re-create your user model according to new keywords, simply delete `user.csv` and update `config.json` with new keywords before running the tool. Otherwise, your user model will be saved for repeated use.
