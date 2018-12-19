import json
import os


def load_file(path: str):
    """
    Load the message file given by Facebook and convert it to an object
    :param path: The system path to the message file
    :return: The data stored in the file
    """
    file = open(path)
    data = json.load(file)
    file.close()
    return data


if __name__ == '__main__':
    user_path = str(os.getcwd()) + "\\" + input("Enter filename: ")
    load_file(user_path)
