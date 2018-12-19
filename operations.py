import re
import datetime


def word_extract(contents: str):
    """
    Seperate words in a string into a list, removing any characters which are uneecessary
    (eg. they're would be considered the same as theyre)
    :param contents: The contents of a message
    :return: A list of the words in contents
    """
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


def timestamp_to_datetime(timestamp: int):
    """
    Convert a timestamp to datetime
    :param timestamp: The timestamp given by Facebook
    :return: The datetime the timestamp corresponds to
    """
    date_time = datetime.datetime.fromtimestamp(timestamp)
    return date_time


def separate_users(data: dict):
    """
    Seperate the messages in the conversation to a dictionary of the people who sent them
    :param data: The messages sent in the conversation
    :return: A dictoinary of the users and the messages they sent
    """
    users = {}
    for user in data['participants']:
        users[user['name']] = []
    for message in data['messages']:
        if message['sender_name'] not in users:
            users[message['sender_name']] = [message]
        else:
            users[message['sender_name']].append(message)
    return users
