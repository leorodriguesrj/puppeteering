from puppet import *

import unittest


class TestParseCommand(unittest.TestCase):
    def test_returns_no_such_command_for_empty_string(self):
        cmd, parameters = parse_command('')
        self.assertEquals(cmd, NO_SUCH_COMMAND)
        self.assertEquals(parameters, ())

    def test_parse_reboot_with_empty_parameter_list(self):
        cmd, parameters = parse_command('{"line":["reboot"]}')
        self.assertEquals(cmd, CMD_REBOOT)
        self.assertEquals(parameters, ())


if __name__ == '__main__':
    unittest.main()
