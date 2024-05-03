import os
import sys
import csv
from .database import FIELDNAMES
from pathlib import Path
from tqdm import tqdm

"""
Register a custom dialect for the CSV module
"""
common_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common"))
if common_path not in sys.path:
    sys.path.append(common_path)
from csv_dialect import get_dialect

db_folder = Path("../db-vulnerable")
output_file = Path("../db-vulnerable.csv")
files = os.listdir(db_folder)

with open(output_file, "w", newline="") as out_file:
    writer = csv.DictWriter(
        out_file,
        fieldnames=FIELDNAMES,
        dialect=get_dialect(),
    )
    writer.writeheader()

    for file in files:
        with open(db_folder / file, "r") as in_file:
            reader = csv.DictReader(
                in_file,
                fieldnames=FIELDNAMES,
                dialect=get_dialect(),
            )
            # Skip header
            next(reader)
            for row in reader:
                writer.writerow(row)
