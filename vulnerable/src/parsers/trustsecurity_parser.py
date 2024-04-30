from selenium.webdriver.common.by import By
from src.helpers.validation_exception import ValidationException
from src.helpers.code import surround_code, require_solidity_code
import re


previous_section = None


# "name", "severity", "function", "description", "recommendation", "impact"
def get_section(text):
    global previous_section

    if not re.match(r"^([A-Z][a-z]*\s?(?:[A-z]*)?):", text):
        return previous_section

    section = None
    if text.startswith("Description:"):
        section = "description"
    elif text.startswith("Recommended Mitigation:"):
        section = "recommendation"
    else:
        section = "unknown"

    previous_section = section
    return section


def group_by_section_and_join(items):
    sections = {}
    for section, parsed_item in items:
        if section not in sections:
            sections[section] = parsed_item["text"]
            continue
        sections[section] += f"\n{parsed_item['text']}"
    return sections


def clear_prefixes(sections):
    for key, value in sections.items():
        sections[key] = re.sub(r"^([A-Z][a-z]*\s?(?:[A-Z][a-z]*)?):\s*", "", value)
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


def parse_markdown_elements(elements):
    require_solidity_code(elements)

    parsed_items = [surround_code(element) for element in elements]
    sections = [get_section(item["text"]) for item in parsed_items]

    items = list(filter(lambda item: item[0] != "unknown", zip(sections, parsed_items)))

    func = extract_function(items)
    sections = group_by_section_and_join(items)
    sections = clear_prefixes(sections)
    sections["function"] = func

    global previous_section
    previous_section = None
    return validate_sections(sections)
