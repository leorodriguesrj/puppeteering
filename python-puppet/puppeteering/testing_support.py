from mock import call

def invocation(magic_mock, *args):
    return [magic_mock.call_args_list, [call(*args)]]