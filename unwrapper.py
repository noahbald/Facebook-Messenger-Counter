import json
import os


def load_file(path):
    file = open(path)
    data = json.load(file)
    return data


if __name__ == '__main__':
    user_path = str(os.getcwd()) + "\\" + input("Enter filename: ")
    load_file(user_path)
