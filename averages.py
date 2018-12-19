import counters


def time_average(messages: dict, output: bool = False, precision: int = 16):
    """
    Calculate the proportions of messages sent in each time frame
    :param messages: The messages in the conversation
    :param output: Whether to print the calculations to the terminal
    :param precision: How many decimal places to consider each proportion
    :return: The proportions of messages sent in each time frame
    """
    time_counts = counters.time_data(messages)
    time_proportions = {}

    for period in time_counts:
        # Calculate the sum of messages send in the time period
        total = sum(time_counts[period])
        # Create a list to store the proportion of each time interval
        proportions = [0] * len(time_counts[period])
        for i in range(len(time_counts[period])):
            if period == "year":
                # If the time period is a type of year, calculate the proportion of messages sent in each year
                total = sum(time_counts[period].values())
                proportions = {}
                for i in time_counts[period]:
                    proportions[i] = round(time_counts[period][i] / total, precision)
                break
            else:
                # Calculate the proportion of messages sent for each interval in the time period
                proportions[i] = round(time_counts[period][i] / total, precision)
        time_proportions[period] = proportions

    if output:
        # Output the data to the terminal
        print("Hour Proportions:", time_proportions['hour'])
        print("Day Proportions:", time_proportions['day'])
        print("Month Proportions:", time_proportions['month'])
        print("Year Proportions:", time_proportions['year'])

    return time_proportions


def call_time_average(messages: dict, output: bool = False):
    """
    Calculate the average length of calls
    :param messages: The messages OF TYPE CALL in the conversation
    :param output: Whether to print the calculations to the console
    :return: The average length of calls
    """
    call_data = counters.call_data(messages)
    average_time = round(call_data['duration_total'] / call_data['answered_count'])

    if output:
        print("Average Call Length:", average_time)

    return average_time


def message_length_average(messages: dict, output: bool = False):
    """
    Calculate the average amount of words in messages
    :param messages: The messages in the conversation
    :param output: Whether to print the calculations to the console
    :return: The average length of messages
    """
    message_data = counters.messages_data(messages)
    average_message_length = round(message_data['message_count'] / message_data['unique_word_count'])

    if output:
        print("Average message length:", average_message_length)

    return average_message_length


def reaction_average(messages: dict, output: bool = False, precision: int = 16):
    """
    Calculate the proportions of reactions made in the conversation
    :param messages: The messages WHICH HAVE REACTIONS in the conversation
    :param output: Whether to print the calculations to the console
    :param precision: How many decimal places to consider each proportion
    :return: The proportions of the reactions made
    """
    react_data = counters.react_data(messages)
    total_reacts = react_data['react_count']
    react_average = {}

    for react in react_data:
        react_average[react] = round(react_data[react] / total_reacts, precision)
        if output:
            print(react, ":", react_average[react])

    return react_average
