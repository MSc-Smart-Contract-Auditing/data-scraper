# data-scraper

Scrape smart contract audits from solodit.xyz

### Usage

1. Create a file `account.json` with the following content:
```json
{
    "email": "Solodit email",
    "password": "Solodit password1234"
}
```

2. Run `./scrape-urls.sh -s {SOURCE}`
- {SOURCE} is the name of the authors of the audit. E.g. `Cyfrin`.
- This will go through all pages of audits and scrape their URLs.
- URLs are saved in `{SOURCE}-urls.csv`

3. Run `./scrape-audits.sh -s {SOURCE}`
- This will go through each URL in `{SOURCE}-urls.csv` and will save the results in `{SOURCE}-data.csv`
