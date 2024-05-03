# Uninstall all compilers of solc
python -m src.uninstall_compilers | xargs rm -r
rm -r contracts
rm audited-urls.csv