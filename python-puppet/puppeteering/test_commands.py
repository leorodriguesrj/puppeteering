from commands import *
from mock import MagicMock, call
from testing_support import *

import unittest


class TestExpandNameValueSequence(unittest.TestCase):
    def test_empty_sequence_expansion(self):
        e = expand_name_value_sequence([])
        self.assertEquals(e, [])

    def test_even_sized_sequence_expansion(self):
        e = expand_name_value_sequence(['a', 'b', 'c', 'd'])
        self.assertEquals(e, [('a', 'b'), ('c', 'd')])
    
    def test_odd_sized_sequence_expansion(self):
        e = expand_name_value_sequence(['a', 'b', 'c', 'd', 'e'])
        self.assertEquals(e, [('a', 'b'), ('c', 'd')])


class TestMakeSetEnvScriptBlock(unittest.TestCase):
    def test_make_script_from_empty_dictionary(self):
        script_block = make_set_env_script_block()
        self.assertEquals(script_block, [
            '',
            ENVBLOCK_START_MARK,
            ENVBLOCK_WARN_NOTICE,
            ENVBLOCK_END_MARK
        ])

    def test_make_script_from_given_values(self):
        script_block = make_set_env_script_block({'name': 'value'})
        self.assertEquals(script_block, [
            '',
            ENVBLOCK_START_MARK,
            ENVBLOCK_WARN_NOTICE,
            'export name="value"',
            ENVBLOCK_END_MARK
        ])


class TestUpdateSystemEnvironment(unittest.TestCase):
    def test_start_and_end_marks_are_found(self):
        make_set_env_script_block_ivk = MagicMock(return_value=['export x=y'])
        save_system_wide_profile_ivk = MagicMock()
        load_system_wide_profile_ivk = MagicMock(return_value=[
            'some instruction',
            ENVBLOCK_START_MARK,
            'export z=a',
            ENVBLOCK_END_MARK,
            'some other instruction'
        ])
        expeced_block = [
            'some instruction',
            'export x=y',
            'some other instruction'
        ]
        update_system_environment('some data',
            make_set_env_script_block=make_set_env_script_block_ivk,
            load_system_wide_profile=load_system_wide_profile_ivk,
            save_system_wide_profile=save_system_wide_profile_ivk)
        self.assertEquals(
            make_set_env_script_block_ivk.call_args_list,
            [call('some data')])
        self.assertEquals(save_system_wide_profile_ivk.call_args_list,
            [call(expeced_block, SYSTEM_PROFILE_PATH)])
    
    def test_start_mark_is_missing(self):
        make_set_env_script_block_ivk = MagicMock(return_value=['export a=b'])
        save_system_wide_profile_ivk = MagicMock()
        load_system_wide_profile_ivk = MagicMock(return_value=[
            'some instruction',
            'export z=a',
            ENVBLOCK_END_MARK,
            'some other instruction'
        ])
        expeced_block = [
            'some instruction',
            'export z=a',
            ENVBLOCK_END_MARK,
            'some other instruction',
            'export a=b',
        ]

        update_system_environment('some data',
            make_set_env_script_block=make_set_env_script_block_ivk,
            load_system_wide_profile=load_system_wide_profile_ivk,
            save_system_wide_profile=save_system_wide_profile_ivk)

        self.assertEquals(*invocation(
            make_set_env_script_block_ivk, 'some data'))
        self.assertEquals(*invocation(
            save_system_wide_profile_ivk, expeced_block, SYSTEM_PROFILE_PATH))
    
    def test_end_mark_is_missing(self):
        make_set_env_script_block_ivk = MagicMock(return_value=['export a=b'])
        save_system_wide_profile_ivk = MagicMock()
        load_system_wide_profile_ivk = MagicMock(return_value=[
            'some instruction',
            ENVBLOCK_START_MARK,
            'export z=a',
            'some other instruction'
        ])
        expeced_block = [
            'some instruction',
            ENVBLOCK_START_MARK,
            'export z=a',
            'some other instruction',
            'export a=b',
        ]

        update_system_environment('some data',
            make_set_env_script_block=make_set_env_script_block_ivk,
            load_system_wide_profile=load_system_wide_profile_ivk,
            save_system_wide_profile=save_system_wide_profile_ivk)

        self.assertEquals(*invocation(
            make_set_env_script_block_ivk, 'some data'))
        self.assertEquals(*invocation(
            save_system_wide_profile_ivk, expeced_block, SYSTEM_PROFILE_PATH))


class TestSetEnv(unittest.TestCase):
    def test_every_thing_works_fine(self):
        env_base = {'home': '/home/x'}
        name_value_sequence = ['proxy', 'localhost:3128']
        expected_env_base = {'home': '/home/x', 'proxy': 'localhost:3128'}

        load_environment_base_ivk = MagicMock(return_value=env_base)
        save_environment_base_ivk = MagicMock()
        update_system_environment_ivk = MagicMock()

        result = set_env(name_value_sequence,
            load_environment_base=load_environment_base_ivk,
            save_environment_base=save_environment_base_ivk,
            update_system_environment=update_system_environment_ivk)

        self.assertEquals(env_base, expected_env_base)
        self.assertEquals(result, COMMAND_SUCCEEDED_MESSAGE)
        self.assertEquals(*invocation(
            save_environment_base_ivk, env_base, JSON_ENVIRONMENT_BASE_PATH))
        self.assertEquals(*invocation(
            update_system_environment_ivk, env_base))

    def test_exception_occurs(self):
        def raise_exception(): raise Exception('thrown on purpose')
        load_environment_base_ivk = MagicMock(side_effect=raise_exception)

        result = set_env([], load_environment_base=load_environment_base_ivk)

        self.assertEquals(result, COMMAND_FAILED_MESSAGE)


if __name__ == '__main__':
    unittest.main()
