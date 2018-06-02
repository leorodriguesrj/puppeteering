import json

NO_SUCH_COMMAND = 0
CMD_REBOOT = 1
CMD_GET_ENV = 2

def translate(command_name):
    if command_name == 'reboot':
        return CMD_REBOOT
    if command_name == 'get_env':
        return CMD_GET_ENV
    return NO_SUCH_COMMAND

def parse_request(request='', translate_name=translate):
    if request == '': return NO_SUCH_COMMAND, ()
    request = json.loads('{"content":%s}' % request)
    content = request['content']
    return translate_name(content[0]), tuple(content[1:])

def run_command(commands):
    return RES_END_OF_BUFFER
