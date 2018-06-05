from subprocess import check_output

import json
import os

COMMAND_SUCCEEDED_MESSAGE = 'End of command: success'
COMMAND_FAILED_MESSAGE = 'End of command: failure'

ENVBLOCK_START_MARK = '# PUPPET ENV BLOCK START'
ENVBLOCK_WARN_NOTICE = '# This block was auto-generated. DO NOT EDIT'
ENVBLOCK_END_MARK = '# PUPPET ENV BLOCK END'

JSON_ENVIRONMENT_BASE_PATH = os.path.expanduser('.puppet-env.json')
SYSTEM_PROFILE_PATH = '/etc/profile'

def load_environment_base(path):
    try:
        with open(path, 'rt') as file:
            return json.load(file)
    except:
        return {}

def save_environment_base(data, path):
    try:
        with open(path, 'wt') as file:
            json.dump(file, data)
    except:
        pass

def load_system_wide_profile(path):
    try:
        with open(path, 'rt') as file:
            return file.readlines().split('\n')
    except:
        return []

def save_system_wide_profile(profile_content, path):
    try:
        with open(path, 'wt') as file:
            file.write(profile_content.join('\n'))
    except:
        pass

def expand_name_value_sequence(sequence):
    end = len(sequence)
    end = end - 1 if end % 2 == 1 else end
    return [tuple(sequence[i:i + 2]) for i in range(0, end, 2)]

def make_set_env_script_block(data={}):
    block_start = ['', ENVBLOCK_START_MARK, ENVBLOCK_WARN_NOTICE]
    block_middle = ['export %s="%s"' % (n, v) for n, v in data.iteritems()]
    block_end = [ENVBLOCK_END_MARK]
    return block_start + block_middle + block_end

def update_system_environment(data,
    make_set_env_script_block=make_set_env_script_block,
    load_system_wide_profile=load_system_wide_profile,
    save_system_wide_profile=save_system_wide_profile):

    profile_content = load_system_wide_profile(SYSTEM_PROFILE_PATH)
    new_block = make_set_env_script_block(data)
    try:
        start_index = profile_content.index(ENVBLOCK_START_MARK)
        end_index = profile_content.index(ENVBLOCK_END_MARK)
        profile_content[start_index:(end_index + 1)] = new_block
    except ValueError:
        profile_content = profile_content + new_block
    save_system_wide_profile(profile_content, SYSTEM_PROFILE_PATH)

def set_env(name_value_sequence,
    load_environment_base=load_environment_base,
    save_environment_base=save_environment_base,
    update_system_environment=update_system_environment):

    try:
        env_base = load_environment_base(JSON_ENVIRONMENT_BASE_PATH)
        for name, value in expand_name_value_sequence(name_value_sequence):
            env_base[name] = value
        save_environment_base(env_base, JSON_ENVIRONMENT_BASE_PATH)
        update_system_environment(env_base)
        return COMMAND_SUCCEEDED_MESSAGE
    except Exception:
        return COMMAND_FAILED_MESSAGE