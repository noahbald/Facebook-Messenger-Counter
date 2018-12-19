import counters


def time_average(messages, output=False, precision=16):
    time_counts = counters.time_data(messages)
    time_proportions = {}

    for period in time_counts:
        total = sum(time_counts[period])
        proportions = [0] * len(time_counts[period])
        for i in range(len(time_counts[period])):
            if period == "year":
                total = sum(time_counts[period].values())
                proportions = {}
                for i in time_counts[period]:
                    proportions[i] = round(time_counts[period][i] / total, precision)
                break
            proportions[i] = round(time_counts[period][i] / total, precision)
        time_proportions[period] = proportions

    if output:
        print("Hour Proportions:", time_proportions['hour'])
        print("Day Proportions:", time_proportions['day'])
        print("Month Proportions:", time_proportions['month'])
        print("Year Proportions:", time_proportions['year'])

    return time_proportions

def call_time_average(messages, output=False):
    call_data = counters.call_data(messages)
    average_time = round(call_data['duration_total'] / call_data['answered_count'])

    if output:
        print("Average Call Length:", average_time)

    return average_time

def message_length_average(messages, output=False):
    message_data = counters.messages_data(messages)
    average_message_length = round(message_data['message_count'] / message_data['unique_word_count'])

    if output:
        print("Average message length:", average_message_length)

    return average_message_length

def reaction_average(messages, output=False, precision = 16):
    react_data = counters.react_data(messages)
    total_reacts = react_data['react_count']
    react_average = {}

    for react in react_data:
        react_average[react] = round(react_data[react] / total_reacts, precision)
        if output:
            print(react, ":", react_average[react])

    return react_average
