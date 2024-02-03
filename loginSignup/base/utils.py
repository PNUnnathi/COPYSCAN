# utils.py

from django.utils.html import escape
import re

def highlight_plagiarized_content(input_text, snippet):
    if input_text and snippet:
        # Escape special characters in the input text
        input_text_escaped = re.escape(input_text)

        # Use a regular expression to find whole words
        pattern = re.compile(rf'\b({input_text_escaped})\b', re.IGNORECASE)

        # Replace each matched word with highlighted version
        highlighted_text = pattern.sub(r'<span style="background-color: yellow;">\1</span>', snippet)

        return highlighted_text
    else:
        return escape(snippet)
