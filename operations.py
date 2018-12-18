import re


def word_extract(contents):
    content = contents.lower()
    # Remove special characters
    for i in range(len(content)):
        if content[i - 2:i] == "\\u":
            content = content[:i - 2] + content[i + 22:]
    # Remove numbers
    numbers = "1234567890'"
    # Remove punctuation
    content = re.sub(r'[^\w\s]', '', content)
    for number in numbers:
        content = content.replace(number, "")
    # Remove redundant characters
    content = content.strip()
    # Separate into words
    content = content.split(" ")

    return content