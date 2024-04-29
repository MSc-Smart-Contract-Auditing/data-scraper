from selenium.webdriver.common.by import By
from src.helpers.validation_exception import ValidationException
import re


def surround_code(element):
    is_code = False
    if element.tag_name == "pre":
        is_code = True
        paragraph = f"""```
{element.text}
```
"""
        paragraph = paragraph.replace("...", "// rest of code")
        paragraph = paragraph.replace(">>", "")
        paragraph = paragraph.replace("@>", "")

        inserted_span_items = element.find_elements(
            By.CSS_SELECTOR, "span.token.prefix.inserted"
        )
        deleted_span_items = element.find_elements(
            By.CSS_SELECTOR, "span.token.prefix.deleted"
        )
        for span in [*inserted_span_items, *deleted_span_items]:
            if span.text == "+":
                paragraph = paragraph.replace(span.text, "// Add the line below\n")
            if span.text == "-":
                paragraph = paragraph.replace(span.text, "// Remove the line below\n")
    else:
        paragraph = element.text
        inline_code_items = element.find_elements(By.TAG_NAME, "code")
        for inline_code in inline_code_items:
            paragraph = paragraph.replace(inline_code.text, f"`{inline_code.text}`")

    return {"text": paragraph, "is_code": is_code}


def group_by_section_and_join(items):
    sections = {}
    for section, parsed_item in items:
        if section not in sections:
            sections[section] = parsed_item["text"]
            continue
        sections[section] += f"\n{parsed_item['text']}"
    return sections


def extract_function(items):
    description_items = filter(lambda item: item[0] == "description", items)
    func_items = list(filter(lambda item: item[1]["is_code"], description_items))

    if len(func_items) == 0:
        raise ValidationException()

    return func_items[0][1]["text"]


def validate_sections(sections):
    mandatory_sections = ["description", "recommendation"]

    for section in mandatory_sections:
        if section not in sections:
            raise ValidationException()

    return sections


next_section = None
is_solidity = False


# "name", "severity", "function", "description", "recommendation", "impact"
# Idea: skip title by returning None, and keep returning "next_section" until a
# new title is encountered
def get_section(text):
    global next_section
    global is_solidity

    if text.startswith("Description"):
        next_section = "description"
        return None

    if text.startswith("Examples"):
        next_section = "description"
        return None

    if text.startswith("Recommendation"):
        next_section = "recommendation"
        return None

    # Just skip filenames
    if ".sol" in text:
        is_solidity = True
        return None

    return next_section


def parse_markdown_elements(elements):
    parsed_items = [surround_code(element) for element in elements]
    sections = [get_section(item["text"]) for item in parsed_items]

    items = list(filter(lambda item: item[0] is not None, zip(sections, parsed_items)))

    func = extract_function(items)
    sections = group_by_section_and_join(items)
    sections["function"] = func

    global is_solidity
    global next_section

    if not is_solidity:
        raise ValidationException()

    is_solidity = False
    next_section = None

    return validate_sections(sections)
