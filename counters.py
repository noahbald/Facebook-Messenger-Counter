import operations


def messages_data(messages: list, output: bool = False):
    """
    Counts the messages and words sent in the conversatoin
    :param messages: The list of messages sent in the conversation
    :param output: Whether to print the calculations to the terminal
    :return: The amount of messages and words sent
    """
    word_count = 0
    unique_words = {}
    for message in messages:
        # Get a list of the words in the message
        content_words = operations.word_extract(message['content'])
        word_count += len(content_words)
        for word in content_words:
            if word in unique_words:
                unique_words[word] += 1
            else:
                unique_words[word] = 1

    if output:
        # Output the data to the console
        print("Total Messages:", len(messages))
        print("Total Words:", word_count)
        print("Unique Words:", len(unique_words))

    return {'message_count': len(messages), 'word_count': word_count, 'unique_word_count': len(unique_words),
            'unique_word_list': unique_words}


def media_data(media: dict, output: bool = False):
    """
    Count the amount of each type of media sent in the conversation
    :param media: The list of messages sent in the conversation
    :param output: Whether to print the calculations to the terminal
    :return:The amount of each type of media
    """
    # A list of the types of media that can be attached to a message
    media_types = ["photos", "videos", "gifs", "files", "audio_files"]

    total_count = 0
    photo_count = 0
    video_count = 0
    audio_count = 0
    files_count = 0
    gifs_count = 0
    # Count each media type
    for item in media:
        # There can be multiple media in one message, so consider the len
        if media_types[0] in item:
            photo_count += len(item[media_types[0]])
            total_count += 1
        elif media_types[1] in item:
            video_count += len(item[media_types[1]])
            total_count += 1
        elif media_types[2] in item:
            gifs_count += len(item[media_types[2]])
            total_count += 1
        elif media_types[3] in item:
            files_count += len(item[media_types[3]])
            total_count += 1
        elif media_types[4] in item:
            audio_count += len(item[media_types[4]])
            total_count += 1

    if output:
        # Output the data to the console
        print("Total Media", total_count)
        print("Photos:", photo_count)
        print("Videos:", video_count)
        print("Gifs:", gifs_count)
        print("Files:", files_count)
        print("Audio:", audio_count)

    return {'media_count': total_count, 'photo_count': photo_count, 'video_count': video_count, 'gif_count': gifs_count,
            'file_count': files_count, 'audio_count': audio_count}


def react_data(reactions: dict, output: bool = False):
    """
    Count the amount of reactions made in the conversation
    :param reactions: The list of messages sent in the conversation WITH REACTIONS
    :param output: Whether to print the calculations to the terminal
    :return: The amount of reactions made
    """
    # The unicode character for the reactions and their names
    react_keys = {"\u00f0\u009f\u0098\u008d": "love", "\u00f0\u009f\u0098\u0086": "laugh",
                  "\u00f0\u009f\u0098\u00ae": "wow", "\u00f0\u009f\u0098\u00a2": "sad",
                  "\u00f0\u009f\u0098\u00a0": "angry", "\u00f0\u009f\u0091\u008d": "like",
                  "\u00f0\u009f\u0091\u008e": "dislike"}

    react_count = 0
    love_count = 0
    laugh_count = 0
    wow_count = 0
    sad_count = 0
    angry_count = 0
    like_count = 0
    dis_i_like_count = 0

    for message in reactions:
        # Go through each message
        reacts = message['reactions']
        react_count += len(reacts)
        for react in reacts:
            # Go through each reaction in the message
            # Get the name of the reaction from the character
            react_key = react_keys[react['reaction']]
            # Determine which react it is and count it
            if react_key == 'love':
                love_count += 1
            elif react_key == 'laugh':
                laugh_count += 1
            elif react_key == 'wow':
                wow_count += 1
            elif react_key == 'sad':
                sad_count += 1
            elif react_key == 'angry':
                angry_count += 1
            elif react_key == 'like':
                like_count += 1
            elif react_key == 'dislike':
                dis_i_like_count += 1
            elif output:
                # This shouldn't happen
                print("unknown reaction")

    if output:
        # Output the data to the console
        print("Total Reacts:", react_count)
        print("Loves:", love_count)
        print("Laugh:", laugh_count)
        print("Wow:", wow_count)
        print("Sad:", sad_count)
        print("Angry:", angry_count)
        print("Like:", like_count)
        print("Dislike:", dis_i_like_count)

    return {'react_count': react_count, 'love_count': love_count, 'laugh_count': laugh_count, 'wow_count': wow_count,
            'sad_count': sad_count, 'angry_count': angry_count, 'like_count': like_count,
            'dislike_count': dis_i_like_count}


def call_data(messages: dict, output: bool = False):
    """
    Calculate the amount of calls made in the conversation
    :param messages: The list of messages WHICH ARE OF TYPE "CALL"
    :param output: Whether to print the calculations to the terminal
    :return: The amount of calls made
    """
    total_duration = 0
    total_calls = len(messages)
    missed_count = 0
    answered_count = 0
    for message in messages:
        if 'missed' in message:
            missed_count += 1
            continue
        answered_count += 1
        total_duration += message['call_duration']

    if output:
        # Output the data to the console
        print("Total Calls:", total_calls)
        print("Total Duration:", total_duration)
        print("Total Missed", missed_count)
        print("Total Answered", answered_count)

    return {'call_count': total_calls, 'duration_total': total_duration, 'missed_count': missed_count,
            'answered_count': answered_count}


def time_data(messages: dict, output: bool = False):
    """
    Count the amount of messages sent in each time-frame in the conversation
    :param messages: The messages sent in the conversation
    :param output: Whether to print the calculations to the terminal
    :return: The amount of messages sent in each time-frame (hours, days, months, and years)
    """
    count_hour = [0] * 24  # 0:00 - 23:00
    count_day = [0] * 7  # mon - tue
    count_month = [0] * 12  # jan-dec
    count_year = {}  # past-present

    for message in messages:
        date_time = None
        # Get the datetime from the time-stamp
        if 'timestamp' in message:
            date_time = operations.timestamp_to_datetime(message['timestamp'])
        elif 'timestamp_ms' in message:
            # Divide the time-stamp by 1000 to interpret it correctly
            date_time = operations.timestamp_to_datetime(message['timestamp_ms']/1000)
        elif date_time is None:
            print("Missing Timestamp\n", message)
            continue
        hour = int(date_time.strftime("%H"))
        day = date_time.weekday()
        month = int(date_time.strftime("%m"))-1
        year = int(date_time.strftime("%Y"))

        count_hour[hour] += 1
        count_day[day] += 1
        count_month[month] += 1
        # Count the year
        if year not in count_year:
            count_year[year] = 1
        else:
            count_year[year] += 1

    if output:
        # Output the data to the console
        print("Hour counts:", count_hour)
        print("Day counts:", count_day)
        print("Month counts:", count_month)
        print("Year counts:", count_year)

    return {'hour': count_hour, 'day': count_day, 'month': count_month, 'year': count_year}
