import json

NO_SUCH_COMMAND = 0
CMD_REBOOT = 1


def translate(command_name):
    if command_name == 'reboot':
        return CMD_REBOOT
    return NO_SUCH_COMMAND


def parse_command(json_text):
    if json_text == '':
        return NO_SUCH_COMMAND, ()
    request = json.loads(json_text)
    line = request['line']
    return translate(line[0]), tuple(line[1:])


def run_command(commands):
    return RES_END_OF_BUFFER
