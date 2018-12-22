import unwrapper
import counters
import averages
import operations
import people
import application

import os
import PyQt5

# Constants
DEFAULT_FILENAME = "message.json"
MEDIA = ["photos", "videos", "gifs", "files", "audio_files"]
REACTS = {"\u00f0\u009f\u0098\u008d": "love", "\u00f0\u009f\u0098\u0086": "laugh",
          "\u00f0\u009f\u0098\u00ae": "wow", "\u00f0\u009f\u0098\u00a2": "sad",
          "\u00f0\u009f\u0098\u00a0": "angry", "\u00f0\u009f\u0091\u008d": "like",
          "\u00f0\u009f\u0091\u008e": "dislike"}

# Global Variables
data = {}
message_types = {}
people_data = {}


def main(mode: str = "application"):
    """
    Runs through the system's main procedures
    :param mode: the I/O mode for the application
    :return: None
    """
    # get gloval data
    global data
    global message_types
    global people_data

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
    message_types = message_distribution()

    # Separate User Data
    people_data = operations.separate_users(data)

    # Run application in the I/O mode selected
    if mode == "legacy":
        # Run the application through the terminal
        menu()
        return
    elif mode == "application":
        application.main(data, message_types, people_data)


def message_distribution():
    """
    Distributes messages into categories
    :return: A dictionary of the categories and their related messages
    """
    # Initialise variables
    global data
    media_type = None
    messages = []
    media = []
    stickers = []
    nickname = []
    group_info = []
    reactions = []
    calls = []
    plans = []
    shares = []

    # Go though each message and place it into it's respective categories
    for message in data['messages']:
        if 'reactions' in message:
            # If the message has reactions, categorise it as so
            reactions.append(message)
        for media_type in MEDIA:
            # If the message is a type of media, categorise it as so
            if media_type in message:
                media.append(message)
                break
        if media_type is not None and media_type in message:
            # If the message was found to be media, move to the next message
            continue
        if 'content' in message:
            content = message['content']
            # Vulnerable to categorising actual messages
            if " set the nickname for " in content or " set your nickname to " in content:
                # If the message was a nickname change, categorise it as so
                nickname.append(message)
                continue
            elif " changed the group photo." in content or " removed the group photo." in content \
                    or " removed the group name." in content or " named the group " in content:
                # If the message was a group info change, categorise it as so
                group_info.append(message)
                continue
        if 'sticker' in message:
            # If the message was a sticker, categorise it as so
            stickers.append(message)
            continue
        elif message['type'] == "Generic" and 'content' in message:
            # If the message was a text message, categorise it as so
            messages.append(message)
        elif message['type'] == "Call":
            # If the message was a call, categorise it as so
            calls.append(message)
        elif message['type'] == "Plan":
            # If the message was a plan, categorise it as so
            plans.append(message)
        elif message['type'] == "Share":
            # If the message was a shared link, categorise it as so
            shares.append(message)

    # Create a dictionary and return it
    return {'messages': messages, 'media': media, 'stickers': stickers, 'nickname': nickname,
            'group_info': group_info, 'reactions': reactions, 'calls': calls, 'plans': plans, 'shares': shares}


def menu():
    """
    A command-line interface to interact with the features of the application
    :return: None
    """
    global message_types

    def get_selection(low: int, high: int):
        """
        Ask the user for a number within a range
        :param low: The lower boundary of the selection
        :param high: The upper boundary of the selection
        :return: The user's selected number
        """
        while True:
            try:
                # Ask the user for a number within the range
                user_selection = int(input("Select a number between [{0} and {1}]: ".format(low, high)))
                if not (low <= user_selection <= high):
                    # If the selection was invalid, try again
                    print("Enter value within range...")
                    continue
                else:
                    break
            except ValueError as e:
                print("Error", e, "try again")
        return user_selection

    print("legacy menu")

    # menu string
    main_menu = "\nMenu:\n\t1. Counters\n\t2. Averages\n\t3. People\n\t4. quit"

    while True:
        # Display the main menu and ask the user's selection
        print(main_menu)
        selection = get_selection(1, 4)
        if selection == 1:  # Counters
            counter_menu = "\nCounter Menu:\n\t1. Messages\n\t2. Media\n\t3. Stickers\n\t4. Others" \
                           "\n\t5. Unique Words\n\t6. Reacts\n\t7. Time Counts\n\t8. Back"
            print(counter_menu)
            selection = get_selection(1, 8)
            if selection == 1:  # Messages
                counters.messages_data(message_types['messages'], output=True)
            elif selection == 2:  # Media
                counters.media_data(message_types['media'], output=True)
            elif selection == 3:  # Stickers
                print("Total Stickers:", len(message_types['stickers']))
            elif selection == 4:  # Others
                print("Total Nickname Changes:", len(message_types['nickname']))
                print(len(message_types['group_info']), "Changes to the group info")
                counters.call_data(message_types['calls'], True)
                print("Total Plans:", len(message_types['plans']))
                print("Total Shares:", len(message_types['shares']))
            elif selection == 5:  # Unique Words
                words = counters.messages_data(message_types['messages'])['unique_word_list']
                while True:
                    # Query user for specific words
                    word = input("Input a word: ")
                    if word == "":
                        # The user did not enter a word; return to menu
                        break
                    if word in words:
                        # If the word is in the conversation, tell the user the number of occurrences
                        print(word, "occurred", words[word], "times")
                    else:
                        # If the word isn't found, tell the user there was zero occurrences
                        print(word, "occurred 0 times")
            elif selection == 6:  # Reacts
                counters.react_data(message_types['reactions'], output=True)
            elif selection == 7:  # Time Counts
                counters.time_data(data['messages'], output=True)
            elif selection == 8:  # Back
                continue
        elif selection == 2:  # Averages
            averages_menu = "\nAverages:\n\t1. Time Average\n\t2. Call length" \
                    "\n\t3. Message length\n\t4. Reaction Proportions\n\t5. Back"
            print(averages_menu)
            selection = get_selection(1, 5)
            if selection == 1:  # Time Average
                averages.time_average(data['messages'], output=True, precision=2)
            elif selection == 2:  # Call length
                averages.call_time_average(message_types['calls'], output=True)
            elif selection == 3:  # Message length (words)
                averages.message_length_average(message_types['messages'], output=True)
            elif selection == 4:  # Reaction Proportions
                averages.reaction_average(message_types['reactions'], output=True, precision=2)
            elif selection == 5:  # Back
                continue
        elif selection == 3:  # People
            people_menu = "\nPeople:\n\t1. People List\n\t2. People Total Messages\n\t3. People Words\n\t" \
                          "4. People Reactions\n\t5. People Calls\n\t6. People Stickers\n\t7. People Media\n\t8. Quit"
            print(people_menu)
            selection = get_selection(1, 8)
            if selection == 1:  # People List
                print(people.names(people_data))
            elif selection == 2:  # People Total Messages
                print(people.people_message_count(people_data))
            elif selection == 3:  # People Words
                print("Word Count:", people.people_word_count(people_data))
                print("Average Word Count:", people.people_word_average(people_data))
            elif selection == 4:  # People Reactions
                people.people_react_count(people_data, message_types['reactions'], True)
            elif selection == 5:  # People Calls
                people.people_call_count(people_data, output=True)
            elif selection == 6:  # People Stickers
                print(people.people_message_type_count(people_data, message_types['stickers']))
            elif selection == 7:  # People Media
                print(people.people_media_count(people_data))
            elif selection == 8:  # back
                continue

        elif selection == 4:  # Quit
            break


if __name__ == '__main__':
    main(mode="application")
