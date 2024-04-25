from selenium.webdriver.common.by import By
from src.helpers.validation_exception import ValidationException
import re


def parse(element):
    is_code = False
    if element.tag_name == "pre":
        is_code = True
        paragraph = f"""
```
{element.text}
```
"""
        paragraph = paragraph.replace("...", "// rest of code")
    else:
        paragraph = element.text
        inline_code_items = element.find_elements(By.TAG_NAME, "code")
        for inline_code in inline_code_items:
            paragraph = paragraph.replace(inline_code.text, f"`{inline_code.text}`")

    return {"text": paragraph, "is_code": is_code}


previous_section = None


# "name", "severity", "function", "description", "recommendation", "impact"
def get_section(text):
    global previous_section

    if not re.match(r"^([A-Z][a-z]*\s?(?:[A-Z][a-z]*)?):", text):
        return previous_section

    section = None
    if text.startswith("Description:"):
        section = "description"
    elif text.startswith("Impact"):
        section = "impact"
    elif text.startswith("Recommended Mitigation:"):
        section = "recommendation"
    elif text.startswith("Exploit:"):
        section = "exploit"
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
    parsed_items = [parse(element) for element in elements]
    sections = [get_section(item["text"]) for item in parsed_items]

    items = list(filter(lambda item: item[0] != "unknown", zip(sections, parsed_items)))

    func = extract_function(items)
    sections = group_by_section_and_join(items)
    sections = clear_prefixes(sections)
    sections["function"] = func
    return validate_sections(sections)
