from parsing import *
from mock import MagicMock, call

import parsing
import unittest


class TestTranslate(unittest.TestCase):
    def test_command_name_is_unknown(self):
        self.assertEquals(translate(''), NO_SUCH_COMMAND)
    
    def test_command_name_is_reboot(self):
        self.assertEquals(translate('reboot'), CMD_REBOOT)
    
    def test_command_name_is_get_env(self):
        self.assertEquals(translate('get_env'), CMD_GET_ENV)


class TestParseRequest(unittest.TestCase):
    def test_returns_no_such_command_for_empty_string(self):
        cmd, parameters = parse_request('')
        self.assertEquals(cmd, NO_SUCH_COMMAND)
        self.assertEquals(parameters, ())

    def test_parse_command_with_empty_parameter_list(self):
        parse_ivk = MagicMock(return_value=112358)
        cmd, parameters = parse_request('["cmd_x"]', parse_ivk)
        self.assertEquals(cmd, 112358)
        self.assertEquals(parameters, ())
        self.assertEquals(parse_ivk.call_count, 1)
        self.assertEquals(parse_ivk.call_args_list, [call('cmd_x')])

    def test_parse_command_parameters(self):
        parse_ivk = MagicMock(return_value=132134)
        cmd, parameters = parse_request('["cmd_y", 42, 7, 1.618033]', parse_ivk)
        self.assertEquals(cmd, 132134)
        self.assertEquals(parameters, (42, 7, 1.618033))
        self.assertEquals(parse_ivk.call_count, 1)
        self.assertEquals(parse_ivk.call_args_list, [call('cmd_y')])

if __name__ == '__main__':
    unittest.main()
