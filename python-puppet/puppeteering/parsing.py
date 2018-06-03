import json
import sys

def empty_command():
    pass

def resolve_command(command_name='empty_command', module=sys.modules[__name__]):
    if hasattr(module, command_name):
        return getattr(module, command_name)
    return empty_command

def parse_request(request='', resolve_command=resolve_command):
    if request == '': return empty_command, ()
    request = json.loads('{"content":%s}' % request)
    content = request['content']
    return resolve_command(content[0]), tuple(content[1:])

def run_command(commands):
    return RES_END_OF_BUFFER
