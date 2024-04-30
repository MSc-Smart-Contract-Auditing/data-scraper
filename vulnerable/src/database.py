import csv
import os

# Use special delimiter to avoid conflicts with commas in the data
csv.register_dialect(
    "mydialect",
    delimiter="ч",
    quoting=csv.QUOTE_MINIMAL,
)


class Database:
    def __init__(self, name):
        file_exists = os.path.isfile(f"../db-vulnerable/{name}-db.csv")
        self.file = open(f"../db-vulnerable/{name}-db.csv", "a")

        fieldnames = [
            "name",
            "severity",
            "description",
            "recommendation",
            "impact",
            "function",
        ]

        self.writer = csv.DictWriter(
            self.file, fieldnames=fieldnames, dialect="mydialect"
        )

        if not file_exists:
            self.writer.writeheader()

    def escape(self, data):
        for key in data:
            data[key] = data[key].replace("\n", "\\n").replace("\r", "")
        return data

    def record(self, data):
        self.writer.writerow(self.escape(data))

    def close(self):
        self.file.close()
