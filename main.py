import unwrapper
import counters

import os

# Constants
DEFAULT_FILENAME = "message.json"
MEDIA = ["photos", "videos", "gifs", "files", "audio_files"]
REACTS = {"\u00f0\u009f\u0098\u008d": "love", "\u00f0\u009f\u0098\u0086":
    "laugh", "\u00f0\u009f\u0098\u00ae": "wow", "\u00f0\u009f\u0098\u00a2": "sad",
    "\u00f0\u009f\u0098\u00a0": "angry", "\u00f0\u009f\u0091\u008d": "like",
    "\u00f0\u009f\u0091\u008e": "dislike"}

# Global Variables
data = {}
word_data = {}


def main(mode="latest"):
    # Import data from message.json
    try:
        data = unwrapper.load_file(str(os.getcwd()) + "\\" + DEFAULT_FILENAME)
    except FileNotFoundError:
        while True:
            try:
                # File could not be found under the default filename, try user input
                print("message.json not found, please enter file path or import file into\n" + str(os.getcwd()))
                input("Press enter to continue...")
                try:
                    data = unwrapper.load_file(str(os.getcwd()) + "\\" + DEFAULT_FILENAME)
                    break
                except FileNotFoundError:
                    data = unwrapper.load_file(input("Enter file path: "))
                    break
            except FileNotFoundError:
                continue

    # Distribute message types
    messages = []; media = []; stickers = []; nickname = []; group_info = []; reactions = []
    for message in data['messages']:
        if 'reactions' in message:
            reactions.append(message)
        for media_type in MEDIA:
            if media_type in message:
                media.append(message)
                break
        if 'content' in message:
            content = message['content']
            # Vulnerable to categorising actual messages
            if " set the nickname for " in content or " set your nickname to " in content:
                nickname.append(message)
                continue
            elif " changed the group photo." in content or " removed the group photo." in content or " removed the group name." in content or " named the group " in content:
                group_info.append(message)
                continue
        if 'sticker' in message:
            stickers.append(message)
            continue
        elif message['type'] == "Generic" and 'content' in message:
            messages.append(message)
            continue

    if mode == "legacy":
        menu([messages, media, stickers, nickname, group_info, reactions])

def menu(types):
    def get_selection(low, high):
        while True:
            try:
                selection = int(input("Select a number between [{0} and {1}]: ".format(low, high)))
                if not (low <= selection <= high):
                    print("Enter value within range...")
                    continue
                break
            except ValueError as e:
                print("Error", e, "try again")
        return selection

    [messages, media, stickers, nickname, group_info, reactions] = types
    print("legacy menu")

    # menu strings
    main_menu = "\nMenu:\n\t1. counters\n\t2. averages\n\t3. quit"

    while True:
        print(main_menu)
        selection = get_selection(1, 3)
        if selection == 1: # Counters
            counter_menu = "\nCounter Menu:\n\t1. Messages\n\t2. Media\n\t3. Stickers\n\t4. Nicknames\n\t" \
                           "5. Group Updates\n\t6. Unique Words\n\t7. Reacts\n\t8. Back"
            print(counter_menu)
            selection = get_selection(1, 8)
            if selection == 1:  # Messages
                counters.messages_data(messages, output=True)
            if selection == 2:  # Media
                counters.media_data(media, output=True)
            if selection == 3:  # Stickers
                print("Total Stickers:", len(stickers))
            if selection == 4:  # Nicknames
                print("Total Nickname Changes:", len(nickname))
            if selection == 5:  # Group Updates
                print(len(group_info), "Changes to the group info")
            if selection == 6:  # Unique Words
                words = counters.messages_data(messages)['unique_word_list']
                while True:
                    word = input("Input a word: ")
                    if word == "":
                        break
                    if word in words:
                        print(word, "occured", words[word], "times")
                    else:
                        print(word, "occured 0 times")
            if selection == 7:  # Reacts
                counters.react_data(reactions, output=True)


        if selection == 2: # Averages
            continue
        if selection == 3: # Quit
            break


if __name__ == '__main__':
    main(mode="legacy")
