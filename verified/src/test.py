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
    adjusted_lines = [line[first_line_indent:] for line in lines[1:]]
    return "\n".join([lines[0]] + adjusted_lines)


# Example usage
file_path = "contracts/DeFiPlaza-0.8.6/Context.sol"
start = 586  # Start byte from the src attribute
length = 143  # Length from the src attribute
source_code_snippet = extract_source_code(file_path, start, length)
print(adjust_indentation(source_code_snippet))
