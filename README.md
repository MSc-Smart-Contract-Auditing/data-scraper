# data-scraper

Scrape smart contract audits from [solodit.xyz](https://solodit.xyz/)

### Usage

## Scraping vulnerable contracts

1. `cd vulnerable` to go to the correct folder
2. Create a file `account.json` with the following content:
```json
{
    "email": "Solodit email",
    "password": "Solodit password1234"
}
```

3. Run `./scrape-urls.sh -s {SOURCE}`
- `{SOURCE}` is the name of the authors of the audit. E.g. `Cyfrin`.
- This will go through all pages of audits and scrape their URLs.
- URLs are saved in `{SOURCE}-urls.csv`

4. Run `./scrape-audits.sh -s {SOURCE}`
- This will go through each URL in `{SOURCE}-urls.csv` and will save the results in `{SOURCE}-db.csv`

## Scraping verified contracts

1. `cd verified`
2. Run `./scrape-urls.sh`. This will scrape the urls of all verified contracts written in `Solidity` with more than 1 ETH
3. Run `./scrape-contracts.sh`. This will scrape the actual contracts. Each contract is saved under a folder with it's name containing all contracts necessary.
4. Run `./prepare-contracts.sh`. This will fix the import statements to prepare the contracts for compilation.
    - ** Do not close the browser or the scraper will crash! **
5. Run `./compile-contracts.sh`
6. Run `./extract-functions.sh`
7. Run `./clean.sh` to uninstall all `solc` compiler versions and remove unnecessary files