from selenium.webdriver.common.by import By
from .validation_exception import ValidationException
import re


def surround_inline(element):
    paragraph = element.text
    inline_code_items = element.find_elements(By.TAG_NAME, "code")
    # Replace inline code with `{code}` only once, hence the set
    inline_code_text_set = {inline_code.text for inline_code in inline_code_items}
    for text_item in inline_code_text_set:
        # Find the text item with space or punctuation boundaries
        # (?<=\s) - positive lookbehind for whitespace
        # (?<=^) - positive lookbehind for start of the string
        # If the text item is followed by punctuation AND witespace it should be included in the match
        # Otherwise it could be `obj.method()` for example
        pattern = rf"(?:(?<=\s)|(?<=^)){re.escape(text_item)}(?=[.?!,]?(\s+|$))"
        replacement = f"`{text_item}`"

        try:
            paragraph = re.sub(pattern, replacement, paragraph)
        except:
            # Fail validation if the regex fails (escaping issues, etc.)
            raise ValidationException()

        paragraph = paragraph.replace(f" {text_item} ", f" `{text_item}` ")

    return paragraph


def parse_codeblock(element):
    paragraph = f"""```
{element.text}
```
"""

    # Cleanup on usual syntax issues
    paragraph = paragraph.replace("...", "// rest of code")
    paragraph = paragraph.replace(">>", "")
    paragraph = paragraph.replace("@>", "")

    # Replace the prefix with a comment
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

    # Remove prefixing line numbers
    paragraph = re.sub(r"^\d+:\s", "", paragraph, flags=re.MULTILINE)

    return paragraph


def surround_code(element):
    # Ignore entirely because it is breaking
    if element.tag_name == "details":
        return {"text": "", "is_code": False}

    is_code = False
    if element.tag_name == "pre":
        is_code = True
        paragraph = parse_codeblock(element)
    else:
        paragraph = surround_inline(element)

    return {"text": paragraph, "is_code": is_code}
