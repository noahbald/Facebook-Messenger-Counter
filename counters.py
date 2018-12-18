import operations


def messages_data(messages, output=False):
    word_count = 0
    unique_words = {}
    for message in messages:
        content_words = operations.word_extract(message['content'])
        word_count += len(content_words)
        for word in content_words:
            if word in unique_words:
                unique_words[word] += 1
            else:
                unique_words[word] = 1

    if output:
        print("Total Messages:", len(messages))
        print("Total Words:", word_count)
        print("Unique Words:", len(unique_words))

    return {'message_count': len(messages), 'word_count': word_count, 'unique_word_count': len(unique_words),
            'unique_word_list': unique_words}

def media_data(media, output=False):
    media_types = ["photos", "videos", "gifs", "files", "audio_files"]

    photo_count = 0
    video_count = 0
    audio_count = 0
    files_count = 0
    gifs_count = 0
    # Count each media type
    for item in media:
        if media_types[0] in item:
            photo_count += len(item[media_types[0]])
        elif media_types[1] in item:
            video_count += len(item[media_types[1]])
        elif media_types[2] in item:
            gifs_count += len(item[media_types[2]])
        elif media_types[3] in item:
            files_count += len(item[media_types[3]])
        elif media_types[4] in item:
            audio_count += len(item[media_types[4]])

    if output:
        print("Total Media", len(media))
        print("Photos:", photo_count)
        print("Videos:", video_count)
        print("Gifs:", gifs_count)
        print("Files:", files_count)
        print("Audio:", audio_count)

    return {'media_count': len(media), 'photo_count': photo_count, 'video_count': video_count, 'gif_count': gifs_count,
            'file_count': files_count, 'audio_count': audio_count}


def react_data(reactions, output=False):
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
        reacts = message['reactions']
        react_count += len(reacts)
        for react in reacts:
            react_key = react_keys[react['reaction']]
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
                print("unknown reaction")

    if output:
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
