import jmespath
import json
import os
from pathlib import Path
import csv
import sys
import os


"""
Register a custom dialect for the CSV module
"""
common_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common"))
if common_path not in sys.path:
    sys.path.append(common_path)
from csv_dialect import get_dialect


def extract_source_code(file_path, start, length):
    with open(file_path, "r", encoding="utf-8") as file:
        file.seek(start)
        function_body = file.read(length)
        # print(function_body)
        return function_body


def adjust_indentation(source_code):
    lines = source_code.split("\n")
    if not lines:
        return source_code

    # Find the first non-whitespace character in the first line to determine the initial indentation
    first_line_indent = len(lines[-1]) - len(lines[-1].lstrip())
    # Adjust all lines to reduce the indentation by the amount found in the first line
    adjusted_lines = []
    for line in lines:
        # If there is witespace in the line
        if len(line) != len(line.lstrip()):
            line = line[first_line_indent:]
        adjusted_lines.append(line)
    return "\n".join(adjusted_lines)


def surround_codeblocks(source_code):
    return f"""```
{source_code}
```
"""


def get_loc(positions):
    return (int(num) for num in positions.split(":")[:2])


def escape(string):
    return string.replace("\n", "\\n").replace("\r", "")


db = open(f"../db-verified", "w")
writer = csv.DictWriter(
    db,
    fieldnames=["function"],
    dialect=get_dialect(),
)
writer.writeheader()

directory = Path("contracts")
for contract in os.listdir(directory):
    files = os.listdir(directory / contract)
    for file in files:
        if file == "out":
            continue
        file_name = file.split(".")[0]

        # Some files do not get compiled to an AST
        try:
            with open(directory / contract / f"out/{file_name}.ast.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            continue

        query = """
            nodes[?nodeType == 'ContractDefinition'].nodes[] | [?nodeType == 'FunctionDefinition' && implemented && !virtual]
        """

        # # Execute JMESPath query
        implemented_functions = jmespath.search(query, data)
        functions_ast = json.loads(json.dumps(implemented_functions, indent=4))

        if not functions_ast:
            continue

        # Example usage
        file_path = directory / contract / file
        for function_obj in functions_ast:
            start, length = get_loc(function_obj["src"])
            source_code_snippet = extract_source_code(file_path, start, length)
            source_code_snippet = adjust_indentation(source_code_snippet)
            source_code_snippet = surround_codeblocks(source_code_snippet)
            source_code_snippet = escape(source_code_snippet)
            writer.writerow({"function": source_code_snippet})

db.close()
