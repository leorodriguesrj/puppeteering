from parsing import *
from mock import MagicMock, call

import parsing
import unittest


class TestResolveCommand(unittest.TestCase):
    def test_name_is_not_given(self):
        self.assertEquals(resolve_command(), empty_command)
    
    def test_name_is_not_found(self):
        self.assertEquals(resolve_command('cmd_x'), empty_command)
    
    def test_name_is_found(self):
        module = __import__('os')
        self.assertEquals(resolve_command('getenv', module), module.getenv)


class TestParseRequest(unittest.TestCase):
    def test_request_is_empty(self):
        cmd, parameters = parse_request('')
        self.assertEquals(cmd, empty_command)
        self.assertEquals(parameters, ())

    def test_request_carries_no_arguments(self):
        parse_ivk = MagicMock(return_value='implementation of cmd_x')
        cmd, parameters = parse_request('["cmd_x"]', parse_ivk)
        self.assertEquals(cmd, 'implementation of cmd_x')
        self.assertEquals(parameters, ())
        self.assertEquals(parse_ivk.call_count, 1)
        self.assertEquals(parse_ivk.call_args_list, [call('cmd_x')])

    def test_request_carries_some_arguments(self):
        parse_ivk = MagicMock(return_value='implementation of cmd_y')
        cmd, parameters = parse_request('["cmd_y", 42, 7, 1.618033]', parse_ivk)
        self.assertEquals(cmd, 'implementation of cmd_y')
        self.assertEquals(parameters, (42, 7, 1.618033))
        self.assertEquals(parse_ivk.call_count, 1)
        self.assertEquals(parse_ivk.call_args_list, [call('cmd_y')])


if __name__ == '__main__':
    unittest.main()
