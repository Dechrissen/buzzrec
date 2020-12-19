# buzzrec
 A content-based filtering recommendation engine for academic papers in linguistics from [LingBuzz](https://ling.auf.net/lingbuzz).

## Installation

Download this repository with the green Code button, or

To download via `git`:
```cmd
 > git clone https://github.com/Dechrissen/buzzrec.git
 ```

## Usage

### Initial setup
Populate `config.json` with the following information:
- your email address,
- keywords that define your interests (`buzzrec` will take these into consideration for its initial data collection).  

For example:
```json
{
  "email" : "john.smith@email.com",
  "keywords" : ["computational phonology", "context free grammars", "french"]
}
```

### Using the tool

`cd` to the `buzzrec` directory, then

```cmd
> python recommender.py
```

### Deleting a user model

To have `buzzrec` to recreate your user model according to new keywords in `config.json`, simply delete the `user.csv` file before running the tool. Otherwise, your user model will be saved for repeated use.
