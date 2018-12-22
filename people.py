import counters
import averages


# Global Variables
REACTS = {"\u00f0\u009f\u0098\u008d": "love", "\u00f0\u009f\u0098\u0086": "laugh",
          "\u00f0\u009f\u0098\u00ae": "wow", "\u00f0\u009f\u0098\u00a2": "sad",
          "\u00f0\u009f\u0098\u00a0": "angry", "\u00f0\u009f\u0091\u008d": "like",
          "\u00f0\u009f\u0091\u008e": "dislike"}


def names(people: dict):
    """
    Return a dict of the names of the people in the conversation
    :param people: The dictionary of the people in the conversation and their messages
    :return: The names of the people in the conversation
    """
    if not isinstance(people, dict):
        raise TypeError("people must be of type dict")
    return [x for x in people.keys()]


def people_message_count(people: dict):
    """
    Return a dict of the amount of messages sent by each person
    :param people: The dictionary of the people in the conversation and their messages
    :return: The amount of messages by each person
    """
    if not isinstance(people, dict):
        raise TypeError("people must be of type dict")
    for data in people.values():
        if not isinstance(data, list):
            raise TypeError("The data for each person must be of type list")
    return {x: len(people[x]) for x in people.keys()}


def people_word_count(people: dict):
    """
    Return a dict of the amount of words sent by each person
    :param people: The dictionary of the people in the conversation and their messages
    :return: The amount of words by each person
    """
    if not isinstance(people, dict):
        raise TypeError("people must be of type dict")
    for data in people.values():
        if not isinstance(data, list):
            raise TypeError("The data for each person must be of type list")
    # Get the message data for each person
    y = {x: counters.messages_data(people[x]) for x in people.keys()}
    # Return omly the word count related data
    return {x: {'word_count': y[x]['word_count'],
                'unique_word_count': y[x]['unique_word_count'],
                'unique_word_list': y[x]['unique_word_list']}
            for x in y}


def people_word_average(people: dict):
    """
    Return a dict of the average amount of words in each message sent by each person
    :param people:The dictionary of the people in the conversation and their messages
    :return: The amount of words by each person
    """
    if not isinstance(people, dict):
        raise TypeError("people must be of type dict")
    for data in people.values():
        if not isinstance(data, list):
            raise TypeError("The data for each person must be of type list")
    return {x: averages.message_length_average(people[x]) for x in people.keys()}


def people_react_count(people: dict, messages: list, output: bool = False):
    """
    Return a dict of the amount of reactions and the types of reactions sent by each person
    :param people: The dictionary of the people in the conversation and their messages
    :param messages: A list of the messages WITH REACTIONS ONLY sent by people in the conversation
    :param output: Whether to print the calculations to the terminal
    :return: The amount of reactions sent by each person
    """
    if not isinstance(people, dict):
        raise TypeError("people must be of type dict")
    if not isinstance(messages, list):
        raise TypeError("messages must be of type list")
    if not isinstance(output, bool):
        raise TypeError("output must be of type bool")
    for message in messages:
        if 'reactions' not in message:
            raise ValueError("all messages in messages must have a reaction")
    for data in people.values():
        if not isinstance(data, list):
            raise TypeError("The data for each person must be of type list")

    # Generate a list of actors
    actors = {x: {} for x in people.keys()}
    for message in messages:
        for reaction in message['reactions']:
            # Add react count if it doesn't exits, otherwise increment it
            if 'react_count' not in actors[reaction['actor']]:
                actors[reaction['actor']]['react_count'] = 1
            else:
                actors[reaction['actor']]['react_count'] += 1
            for react in REACTS:
                # Add react if it doesn't exist, otherwise increment it
                if react == reaction['reaction']:
                    if REACTS[react] not in actors[reaction['actor']]:
                        actors[reaction['actor']][REACTS[react]] = 1
                    else:
                        actors[reaction['actor']][REACTS[react]] += 1
    # Include reactions for actors which were not found
    for actor in actors:
        for react in REACTS.values():
            if react not in actors[actor]:
                actors[actor][react] = 0

    if output:
        # Output data to the terminal
        for actor in actors.keys():
            print(actor)
            for react in actors[actor]:
                if react == 'react_count':
                    print("\tTotal Reactions:", actors[actor][react])
                else:
                    print("\t", react + ":", actors[actor][react])

    return actors


def people_call_count(people: dict, output: bool = False):
    """
    Return a dict of the amount and length of calls made by each person
    :param people: The  dictionary of the people in the conversation and their messages
    :param output: Whether to print the calculations to the terminal
    :return: The amount of calls made by each person
    """
    if not isinstance(people, dict):
        raise TypeError("people must be of type dict")
    if not isinstance(output, bool):
        raise TypeError("output must be of type bool")
    for data in people.values():
        if not isinstance(data, list):
            raise TypeError("The data for each person must be of type list")

    people_calls = people.copy()
    for person in people_calls:
        for i in range(len(people_calls[person]), 0, -1):
            if people_calls[person][i - 1]['type'] != "Call":
                # Remove messages from list that aren't calls
                people_calls[person].pop(i - 1)
    # Get the call data for each person
    people_calls = {x: counters.call_data(people[x]) for x in [y for y in people_calls]}

    if output:
        # Output data to the terminal
        for person in people_calls:
            print(person)
            print("\tTotal Calls:", people_calls[person]['call_count'])
            print("\tTotal Duration:", people_calls[person]['duration_total'])
            print("\tCalls Missed:", people_calls[person]['missed_count'])
            print("\tCalls Answered:", people_calls[person]['answered_count'])

    return people_calls


def people_message_type_count(people: dict, messages_type: list, output: bool = False):
    """
    Return a dict of the amount of messages sent of the particular message_type
    :param people: The dictionary of the people in the conversation and their messages
    :param messages_type: A list of the messages, which may be a particular type
    :param output: Whether to print the calculations to the terminal
    :return: The amount of messeges of that type by each person
    """
    if not isinstance(people, dict):
        raise TypeError("people must be of type dict")
    if not isinstance(messages_type, list):
        raise TypeError("messages_type must be of type list")
    if not isinstance(output, bool):
        raise TypeError("output must be of type bool")
    for data in people.values():
        if not isinstance(data, list):
            raise TypeError("The data for each person must be of type list")

    # Create a dictionary to store each persons count
    senders = {x: 0 for x in people.keys()}
    for message in messages_type:
        for sender in senders:
            if message['sender_name'] == sender:
                # Count the message for the sender
                senders[sender] += 1

    if output:
        # Output data to the terminal
        print(senders)

    return senders


def people_media_count(people: dict):
    """
    Return a dict of the amount of media sent by each person
    :param people: The dict of the people in the conversation and their messages
    :return: The amount of media sent by each person
    """
    if not isinstance(people, dict):
        raise TypeError("people must be of type dict")
    for data in people.values():
        if not isinstance(data, list):
            raise TypeError("The data for each person must be of type list")
    return {x: counters.media_data(people[x]) for x in people.keys()}
