from puppet import *

import unittest


class TestParseCommand(unittest.TestCase):
    def test_returns_no_such_command_for_empty_string(self):
        cmd, parameters = parse_command('')
        self.assertEquals(cmd, NO_SUCH_COMMAND)
        self.assertEquals(parameters, ())

    def test_parse_reboot_with_empty_parameter_list(self):
        cmd, parameters = parse_command('["reboot"]')
        self.assertEquals(cmd, CMD_REBOOT)
        self.assertEquals(parameters, ())
    
    def test_parse_reboot_with_delay_without_scale(self):
        cmd, parameters = parse_command('["reboot", 42]')
        self.assertEquals(cmd, CMD_REBOOT)
        self.assertEquals(parameters, (42,))

    def test_parse_reboot_with_delay_and_scale(self):
        cmd, parameters = parse_command('["reboot", 42, "ms"]')
        self.assertEquals(cmd, CMD_REBOOT)
        self.assertEquals(parameters, (42, 'ms'))


if __name__ == '__main__':
    unittest.main()
