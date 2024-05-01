import jmespath
import json


def extract_source_code(file_path, start, length):
    with open(file_path, "r", encoding="utf-8") as file:
        file.seek(start)
        return file.read(length)


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


def get_loc(positions):
    return (int(num) for num in positions.split(":")[:2])


# Example JSON data (assuming it's already loaded into a variable `data`)

with open("contracts/TokenRedemption-0.8.19/out/Context.ast.json", "r") as file:
    data = json.load(file)


query = """
nodes[?nodeType == 'ContractDefinition'].nodes[] | [?nodeType == 'FunctionDefinition' && implemented].{
    name: name,
    src: src
}
"""

# # Execute JMESPath query
implemented_functions = jmespath.search(query, data)
functions_ast = json.loads(json.dumps(implemented_functions, indent=4))

# Example usage
file_path = "contracts/TokenRedemption-0.8.19/Context.sol"

for function_obj in functions_ast:
    start, length = get_loc(function_obj["src"])
    source_code_snippet = extract_source_code(file_path, start, length)
    print(adjust_indentation(source_code_snippet))
