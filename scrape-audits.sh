#!/bin/bash

# Initialize a variable for the source argument.
SOURCE=""

# Process command-line arguments.
while getopts ":s:" opt; do
  case $opt in
    s)
      SOURCE="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Check if SOURCE is not empty.
if [[ -z "$SOURCE" ]]; then
    echo "You must provide a source with -s"
    exit 1
fi

# Run the scrape_audit.py module with the source argument.
python -m src.scrape_audit -s "$SOURCE"
