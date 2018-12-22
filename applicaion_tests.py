import unittest

import people
import averages
import counters


class CountersTest(unittest.TestCase):
    """
    Tests for counters module
    """

    def setUp(self):
        self.counters_module = counters

    def test_messages_data(self):
        # message_count: 3, word_count: 3, unique_word_count: 2, unique_word_list: {'hello': 2, 'bye': 1}
        dummy_messages = [{'content': "hello, 1 !--   HELLO"},
                          {'content': 'bye'},
                          {'content': ''}]
        # Raises TypeError
        dummy_messages_invalid_type = {0: {'content': "hello, 1 !--   HELLO"}}
        # Raises ValueError
        dummy_messages_missing_content = [{'content': "hello"}, {}]

        # Check valid input
        output = self.counters_module.messages_data(dummy_messages)
        self.assertEqual(output['message_count'], 3)
        self.assertEqual(output['word_count'], 3)
        self.assertEqual(output['unique_word_count'], 2)
        self.assertEqual(output['unique_word_list']['hello'], 2)
        self.assertEqual(output['unique_word_list']['bye'], 1)

        # Check input verification
        with self.assertRaises(TypeError):
            self.counters_module.messages_data(dummy_messages_invalid_type)
        with self.assertRaises(TypeError):
            self.counters_module.messages_data(dummy_messages, None)
        with self.assertRaises(ValueError):
            self.counters_module.messages_data(dummy_messages_missing_content)

    def test_media_data(self):
        # media_count: 5, photo_count: 1, video_count: 1, gif_count: 1, file_count: 1, audio_count: 1
        dummy_media = [{'photos': [None]}, {'videos': [None]}, {'gifs': [None]}, {'files': [None]},
                       {'audio_files': [None]}, {}]
        # Raises TypeError
        dummy_media_invalid_type = {0: {'photos': None}}

        # Check valid input
        output = self.counters_module.media_data(dummy_media)
        self.assertEqual(output['media_count'], 5)
        self.assertEqual(output['photo_count'], 1)
        self.assertEqual(output['video_count'], 1)
        self.assertEqual(output['gif_count'], 1)
        self.assertEqual(output['file_count'], 1)
        self.assertEqual(output['audio_count'], 1)

        # Check input verification
        with self.assertRaises(TypeError):
            self.counters_module.media_data(dummy_media_invalid_type)
        with self.assertRaises(TypeError):
            self.counters_module.media_data(dummy_media, None)

    def test_react_data(self):
        # react_count : 7, love_count: 1, laugh_count: 1, wow_count: 1, sad_count: 1, angry_count: 1,
        # like_count: 1, dislike_count: 1
        dummy_reactions = [{'reactions': [{'reaction': "\u00f0\u009f\u0098\u008d"},
                                          {'reaction': "\u00f0\u009f\u0098\u0086"},
                                          {'reaction': "\u00f0\u009f\u0098\u00ae"},
                                          {'reaction': "\u00f0\u009f\u0098\u00a2"},
                                          {'reaction': "\u00f0\u009f\u0098\u00a0"},
                                          {'reaction': "\u00f0\u009f\u0091\u008d"},
                                          {'reaction': "\u00f0\u009f\u0091\u008e"}]}]
        # Raises TypeError
        dummy_reactions_invalid_type = {0: {'reactions': [{'reaction': "\u00f0\u009f\u0091\u008e", 'actor': ""}]}}
        # Raises ValueError
        dummy_reactions_missing_reaction = [{}]

        # Check valid input
        output = self.counters_module.react_data(dummy_reactions)
        self.assertEqual(output['react_count'], 7)
        self.assertEqual(output['love_count'], 1)
        self.assertEqual(output['laugh_count'], 1)
        self.assertEqual(output['wow_count'], 1)
        self.assertEqual(output['sad_count'], 1)
        self.assertEqual(output['angry_count'], 1)
        self.assertEqual(output['like_count'], 1)
        self.assertEqual(output['dislike_count'], 1)

        # Check input verification
        with self.assertRaises(TypeError):
            self.counters_module.react_data(dummy_reactions_invalid_type)
        with self.assertRaises(ValueError):
            self.counters_module.react_data(dummy_reactions_missing_reaction)
        with self.assertRaises(TypeError):
            self.counters_module.react_data(dummy_reactions, None)

    def test_call_data(self):
        # call_count: 2, duration_total: 30, missed_count: 1, answered_count: 1
        dummy_calls = [{'type': "Call", 'call_duration': 30}, {'type': "Call", 'call_duration': 0, 'missed': True}]

        # Raises TypeError
        dummy_calls_invalid_type = {0: {'type': "Call", 'call_duration': 30}}

        # Raises ValueError
        dummy_calls_missing_call = [{'type': "Call", 'call_duration': 30}, {'type': "Generic", 'call_duration': 30}]

        # Check valid input
        output = self.counters_module.call_data(dummy_calls)
        self.assertEqual(output['call_count'], 2)
        self.assertEqual(output['duration_total'], 30)
        self.assertEqual(output['missed_count'], 1)
        self.assertEqual(output['answered_count'], 1)

        # Check input verification
        with self.assertRaises(TypeError):
            self.counters_module.call_data(dummy_calls_invalid_type)
        with self.assertRaises(ValueError):
            self.counters_module.call_data(dummy_calls_missing_call)
        with self.assertRaises(TypeError):
            self.counters_module.call_data(dummy_calls, None)

    def test_time_data(self):
        # hour: [8: 1, 11: 1], day: [0: 1, 1: 1], month: [5: 1, 11: 1], year: {2018: 1, 2020: 1}
        dummy_times = [{'timestamp': 1545686130}, {'timestamp_ms': 1592185515500}]

        # Raises TypeError
        dummy_times_invalid_type = {0: {'timestamp': 1577881830}}

        # Raises ValueError
        dummy_time_missing_time = [{}]

        # Check valid input
        output = self.counters_module.time_data(dummy_times)
        self.assertEqual(output['hour'], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(output['day'], [1, 1, 0, 0, 0, 0, 0])
        self.assertEqual(output['month'], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1])
        self.assertEqual(output['year'], {2018: 1, 2020: 1})

        # Check input verification
        with self.assertRaises(TypeError):
            self.counters_module.time_data(dummy_times_invalid_type)
        with self.assertRaises(ValueError):
            self.counters_module.time_data(dummy_time_missing_time)
        with self.assertRaises(TypeError):
            self.counters_module.time_data(dummy_times, None)


class AveragesTest(unittest.TestCase):
    """
    Test averages module
    """

    def setUp(self):
        self.averages_module = averages

    def test_time_average(self):
        # hour: [8: 0.5, 11: 0.5], day: [0: 0.5, 1: 0.5], month: [5: 0.5, 11: 0.5], year: {2018: 0.4, 2020: 0.5}
        dummy_times = [{'timestamp': 1545686130}, {'timestamp_ms': 1592185515500}]

        # Raises TypeError
        dummy_time_invalid_type = {0: {'timestamp': 1545686130}}

        # Raises ValueError
        dummy_times_missing_timestamp = [{}]

        # Check valid input
        output = self.averages_module.time_average(dummy_times)
        self.assertEqual(output['hour'], [0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(output['day'], [0.5, 0.5, 0, 0, 0, 0, 0])
        self.assertEqual(output['month'], [0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0.5])
        self.assertEqual(output['year'], {2018: 0.5, 2020: 0.5})

        # Check input verification
        with self.assertRaises(TypeError):
            self.averages_module.time_average(dummy_time_invalid_type)
        with self.assertRaises(ValueError):
            self.averages_module.time_average(dummy_times_missing_timestamp)
        with self.assertRaises(TypeError):
            self.averages_module.time_average(dummy_times, output=None)
        with self.assertRaises(TypeError):
            self.averages_module.time_average(dummy_times, precision=1.0)

    def test_call_time_average(self):
        # average_time = 30
        dummy_calls = [{'type': "Call", 'call_duration': 30}, {'type': "Call", 'call_duration': 0, 'missed': True}]

        # Raises TypeError
        dummy_calls_invalid_type = {0: {'type': "Call", 'call_duration': 30}}

        # Raises ValueError
        dummy_calls_incorrect_type = [{'type': "Generic", 'call_duration': 30}]

        # Check valid input
        output = self.averages_module.call_time_average(dummy_calls)
        self.assertEqual(output, 30)

        # Check input verification
        with self.assertRaises(TypeError):
            self.averages_module.call_time_average(dummy_calls_invalid_type)
        with self.assertRaises(ValueError):
            self.averages_module.call_time_average(dummy_calls_incorrect_type)
        with self.assertRaises(TypeError):
            self.averages_module.call_time_average(dummy_calls, output=None)

    def test_message_length_average(self):
        # average_message_length = 2
        dummy_messages = [{'content': "hello, 1 !--   HELLO"},
                          {'content': 'bye'},
                          {'content': ''}]

        # Raises TypeError
        dummy_messages_invalid_type = {0: {'content': "hello, 1 !--  HELLO"}}

        # Raises ValueError
        dummy_messages_missing_content = [{'content': "hello"}, {}]

        # Check valid input
        output = self.averages_module.message_length_average(dummy_messages)
        self.assertEqual(output, 2)

        # Check zero division
        output = self.averages_module.message_length_average([{'content': ""}])
        self.assertEqual(output, 0)

        # Check input verification
        with self.assertRaises(TypeError):
            self.averages_module.message_length_average(dummy_messages_invalid_type)
        with self.assertRaises(ValueError):
            self.averages_module.message_length_average(dummy_messages_missing_content)
        with self.assertRaises(TypeError):
            self.averages_module.message_length_average(dummy_messages, output=None)

    def test_reaction_average(self):
        # love_count: 1/7, laugh_count: 1/7, wow_count: 1/7, sad_count: 1/7, angry_count: 1/7, like_count: 1/7
        # dislike_count: 1/7
        dummy_reactions = [{'reactions': [{'reaction': "\u00f0\u009f\u0098\u008d"},
                                          {'reaction': "\u00f0\u009f\u0098\u0086"},
                                          {'reaction': "\u00f0\u009f\u0098\u00ae"},
                                          {'reaction': "\u00f0\u009f\u0098\u00a2"},
                                          {'reaction': "\u00f0\u009f\u0098\u00a0"},
                                          {'reaction': "\u00f0\u009f\u0091\u008d"},
                                          {'reaction': "\u00f0\u009f\u0091\u008e"}]}]

        # Raises TypeError
        dummy_reactions_invalid_type = {0: {'reactions': [{'reaction': "\u00f0\u009f\u0091\u008e", 'actor': ""}]}}

        # Raises ValueError
        dummy_reactions_missing_reaction = [{}]

        # Check valid input
        output = self.averages_module.reaction_average(dummy_reactions)
        self.assertAlmostEqual(output['love_count'], 1/7)
        self.assertAlmostEqual(output['laugh_count'], 1/7)
        self.assertAlmostEqual(output['wow_count'], 1/7)
        self.assertAlmostEqual(output['sad_count'], 1/7)
        self.assertAlmostEqual(output['angry_count'], 1/7)
        self.assertAlmostEqual(output['like_count'], 1/7)
        self.assertAlmostEqual(output['dislike_count'], 1/7)

        # Check input verification
        with self.assertRaises(TypeError):
            self.averages_module.reaction_average(dummy_reactions_invalid_type)
        with self.assertRaises(ValueError):
            self.averages_module.reaction_average(dummy_reactions_missing_reaction)
        with self.assertRaises(TypeError):
            self.averages_module.reaction_average(dummy_reactions, output=None)
        with self.assertRaises(TypeError):
            self.averages_module.reaction_average(dummy_reactions, precision=16.0)


class PeopleTests(unittest.TestCase):
    """
    Test people module
    """

    def setUp(self):
        self.people_module = people

    def test_names(self):
        # ['Actor 1', 'Actor 2']
        dummy_people = {'Actor 1': None, 'Actor 2': None}

        # Raises TypeError
        dummy_people_invalid_type = ['Actor 1', 'Actor 2']

        # Check valid input
        output = self.people_module.names(dummy_people)
        self.assertTrue('Actor 1' in output)
        self.assertTrue('Actor 2' in output)
        self.assertEqual(len(output), 2)

        # Check input verification
        with self.assertRaises(TypeError):
            self.people_module.names(dummy_people_invalid_type)

    def test_people_message_count(self):
        dummy_people = {'Actor 1': [None, None], 'Actor 2': [None]}

        # Raises TypeError
        dummy_people_invalid_type = [[{}]]

        # Raises TypeError
        dummy_people_invalid_content = {None: {}}

        # Check valid input
        output = self.people_module.people_message_count(dummy_people)
        self.assertEqual(output['Actor 1'], 2)
        self.assertEqual(output['Actor 2'], 1)

        # Check input verification
        with self.assertRaises(TypeError):
            self.people_module.people_message_count(dummy_people_invalid_type)
        with self.assertRaises(TypeError):
            self.people_module.people_message_count(dummy_people_invalid_content)

    def test_people_word_count(self):
        # Actor 1 {word_count: 3, unique_word_count: 2, unique_word_list: {'hello': 1, 'bye': 2}}
        # Actor 2 {word_count: 0, unique_word_count: 0, unique_word_list: {}}
        dummy_people = {'Actor 1': [{'content': "hello bye bye"}], 'Actor 2': [{'content': ""}, {'content': ""}]}

        # Raises TypeError
        dummy_people_invalid_type = [[{}]]

        # Raises TypeError
        dummy_people_invalid_content = {None: {}}

        # Check valid input
        output = self.people_module.people_word_count(dummy_people)
        self.assertEqual(output['Actor 1']['word_count'], 3)
        self.assertEqual(output['Actor 1']['unique_word_count'], 2)
        self.assertEqual(output['Actor 1']['unique_word_list']['hello'], 1)
        self.assertEqual(output['Actor 1']['unique_word_list']['bye'], 2)
        self.assertEqual(len(output['Actor 1']['unique_word_list']), 2)
        self.assertEqual(output['Actor 2']['word_count'], 0)
        self.assertEqual(output['Actor 2']['unique_word_count'], 0)
        self.assertEqual(len(output['Actor 2']['unique_word_list']), 0)
        self.assertEqual(len(output), 2)

        # Check input verification
        with self.assertRaises(TypeError):
            self.people_module.people_word_count(dummy_people_invalid_type)
        with self.assertRaises(TypeError):
            self.people_module.people_word_count(dummy_people_invalid_content)

    def test_people_word_average(self):
        # Actor 1: 2, Actor 2: 0
        dummy_people = {'Actor 1': [{'content': "a a"}, {'content': "a"}], 'Actor 2': [{'content': ""}]}

        # Raises TypeError
        dummy_people_invalid_type = [[{}]]

        # Raises TypeError
        dummy_people_invalid_content = {None: {}}

        # Check valid input
        output = self.people_module.people_word_average(dummy_people)
        self.assertEqual(output['Actor 1'], 2)
        self.assertEqual(output['Actor 2'], 0)
        self.assertEqual(len(output), 2)

        # Check input verification
        with self.assertRaises(TypeError):
            self.people_module.people_word_average(dummy_people_invalid_type)
        with self.assertRaises(TypeError):
            self.people_module.people_word_average(dummy_people_invalid_content)

    def test_people_react_count(self):
        # Actor 1: {'dislike': 1, ...}
        dummy_people = {'Actor 1': []}
        dummy_messages = [{'reactions': [{'reaction': "\u00f0\u009f\u0091\u008e", 'actor': "Actor 1"}]}]

        # Raises TypeError
        dummy_people_invalid_type = [[{}]]
        dummy_messages_invalid_type = {0: {'reactions': [{'reaction': "\u00f0\u009f\u0091\u008e", 'actor': "Actor 1"}]}}

        # Raises ValueError
        dummy_messages_missing_reaction = [{'reactions': [{'reaction': "\u00f0\u009f\u0091\u008e", 'actor': "Actor 1"}]}, {}]

        # Check valid input
        output = self.people_module.people_react_count(dummy_people, dummy_messages)
        for key in output['Actor 1']:
            if key == 'dislike' or key == 'react_count':
                self.assertEqual(output['Actor 1'][key], 1)
            else:
                self.assertEqual(output['Actor 1'][key], 0)
        self.assertEqual(len(output), 1)

        # Check input verification
        with self.assertRaises(TypeError):
            self.people_module.people_react_count(dummy_people_invalid_type, dummy_messages)
        with self.assertRaises(TypeError):
            self.people_module.people_react_count(dummy_people, dummy_messages_invalid_type)
        with self.assertRaises(ValueError):
            self.people_module.people_react_count(dummy_people, dummy_messages_missing_reaction)
        with self.assertRaises(TypeError):
            self.people_module.people_react_count(dummy_people, dummy_messages, None)

    def test_people_call_count(self):
        # Actor 1: {'call_count': 1, 'duration_total': 30, 'missed_count': 0, 'answered_count': 1}
        # Actor 2: {'call_count': 1, 'duration_total': 0, 'missed_count': 1, 'answered_count': 0)
        dummy_people = {'Actor 1': [{'type': "Call", 'call_duration': 30}],
                        'Actor 2': [{'type': "Call", 'call_duration': 0, 'missed': True}]}

        # Raises TypeError
        dummy_people_invalid_type = [[{}]]

        # Raises TypeError
        dummt_people_invalid_content = {'Actor 1': {'type': "Generic", 'call_duration': 30}}

        # Check valid input
        output = self.people_module.people_call_count(dummy_people)
        self.assertEqual(output['Actor 1']['call_count'], 1)
        self.assertEqual(output['Actor 1']['duration_total'], 30)
        self.assertEqual(output['Actor 1']['missed_count'], 0)
        self.assertEqual(output['Actor 1']['answered_count'], 1)
        self.assertEqual(output['Actor 2']['call_count'], 1)
        self.assertEqual(output['Actor 2']['duration_total'], 0)
        self.assertEqual(output['Actor 2']['missed_count'], 1)
        self.assertEqual(output['Actor 2']['answered_count'], 0)
        self.assertEqual(len(output), 2)

        # Check input verification
        with self.assertRaises(TypeError):
            self.people_module.people_call_count(dummy_people_invalid_type)
        with self.assertRaises(TypeError):
            self.people_module.people_call_count(dummt_people_invalid_content)
        with self.assertRaises(TypeError):
            self.people_module.people_call_count(dummy_people, output=None)

    def test_people_message_type_count(self):
        # Actor 1: 2, Actor 2: 1, Actor 3: 0
        dummy_people = {'Actor 1': [], 'Actor 2': [], 'Actor 3': []}
        dummy_messages_type = [{'sender_name': "Actor 1"}, {'sender_name': "Actor 2"}, {'sender_name': "Actor 2"}]

        # Raises TypeError
        dummy_people_invalid_type = [[{}]]
        dummy_messages_type_invalid_type = {0: {'sender_name': "Actor 1"}}
        dummy_people_invalid_contents = {'Actor 1': None}

        # Check valid input
        output = self.people_module.people_message_type_count(dummy_people, dummy_messages_type)
        self.assertEqual(output['Actor 1'], 1)
        self.assertEqual(output['Actor 2'], 2)
        self.assertEqual(output['Actor 3'], 0)
        self.assertEqual(len(output), 3)

        # Check input verification
        with self.assertRaises(TypeError):
            self.people_module.people_message_type_count(dummy_people_invalid_type, dummy_messages_type)
        with self.assertRaises(TypeError):
            self.people_module.people_message_type_count(dummy_people, dummy_messages_type_invalid_type)
        with self.assertRaises(TypeError):
            self.people_module.people_message_type_count(dummy_people_invalid_contents, dummy_messages_type)
        with self.assertRaises(TypeError):
            self.people_module.people_message_type_count(dummy_people, dummy_messages_type, output=None)

    def test_people_media_count(self):
        # Actor 1: photo_count: 2, Actor 2: video_count = 1, Actpr 3: nothing
        dummy_people = {'Actor 1': [{'photos': [None, None]}], 'Actor 2': [{'videos': [None]}], 'Actor 3': [{}]}

        # TypeError
        dummy_people_invalid_type = [[{}]]

        # Check valid input
        output = self.people_module.people_media_count(dummy_people)
        self.assertEqual(output['Actor 1']['photo_count'], 2)
        self.assertEqual(output['Actor 1']['media_count'], 2)
        self.assertEqual(output['Actor 2']['video_count'], 1)
        self.assertEqual(output['Actor 2']['media_count'], 1)
        self.assertEqual(output['Actor 3']['media_count'], 0)
        self.assertEqual(sum(output['Actor 1'].values()), 4)
        self.assertEqual(sum(output['Actor 2'].values()), 2)
        self.assertEqual(sum(output['Actor 3'].values()), 0)

        # Check input verification
        with self.assertRaises(TypeError):
            self.people_module.people_media_count(dummy_people_invalid_type)


if __name__ == '__main__':
    unittest.main()
