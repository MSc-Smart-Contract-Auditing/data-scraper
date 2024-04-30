if [ ! -d "contracts" ]; then
    mkdir -p "contracts"
fi

python -m src.scrape_contract
