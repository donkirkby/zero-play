import re

from markdown import markdown  # type: ignore

HEADER_PATTERN = re.compile(r'---\s*title:(.*\s*)---')


def convert_markdown(raw_markdown: str) -> str:
    processed_markdown = HEADER_PATTERN.sub(r'# \1', raw_markdown)
    return markdown(processed_markdown)
