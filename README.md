# buzzrec
 A content-based filtering recommendation engine for academic papers in linguistics from [LingBuzz](https://ling.auf.net/lingbuzz).

## Usage
Populate `config.json` with the following information:
- your email address,
- keywords that define your interests (`buzzrec` will take these into consideration for its initial data collection).  

For example:
```json
{
  "email" : "john.smith@email.com",
  "keywords" : ["syntax", "computational phonology", "context free grammars", "french"]
}
```
