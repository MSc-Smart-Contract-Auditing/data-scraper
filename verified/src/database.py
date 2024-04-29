from selenium.webdriver.common.by import By
import csv


class Row:
    def __init__(self, element):
        raw_columns = element.find_elements(By.TAG_NAME, "td")

        self.url = element.find_element(By.TAG_NAME, "a").get_attribute("href")

        (
            self.name,
            self.compiler,
            self.compiler_version,
            self.balance,
        ) = Row._parse(raw_columns)

    def __str__(self):
        return f"{self.name} ({self.compiler} {self.compiler_version}) - {self.balance} ETH"

    def json(self):
        return {
            "compiler_version": self.compiler_version,
            "url": self.url,
        }

    @staticmethod
    def _parse(columns):
        return (
            columns[1].text,
            columns[2].text,
            columns[3].text,
            float(columns[4].text.split()[0].replace(",", "")),
        )


class Database:
    def __init__(self):
        self.rows = []

    def addElementsAndFilter(self, elements):

        rows = [Row(element) for element in elements]
        rows = filter(lambda row: "Solidity" in row.compiler, rows)
        rows = filter(lambda row: row.balance >= 1, rows)

        self.rows.extend(rows)

    def __str__(self):
        return f"===== {len(self)} elements =====\n" + "\n".join(
            str(row) for row in self.rows
        )

    def __len__(self):
        return len(self.rows)

    def escape(self, data):
        for key in data:
            data[key] = data[key].replace("\n", "\\n").replace("\r", "")
        return data

    def save(self):
        fieldnames = ["compiler_version", "url"]

        with open(
            f"verified/audited-urls.csv", "w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            [writer.writerow(row.json()) for row in self.rows]
