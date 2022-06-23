"""Utility functions for dealing with env variables and reading variables from env file"""
import os
import logging
import argparse

telegraf_config_file = 'telegraf.conf'
telegraf_config_file_template = 'telegraf_template.conf'

parser = argparse.ArgumentParser()
parser.add_argument("-env", "--env", help = "Path of env file.")
args = parser.parse_args()

# Read arguments from command line
args = parser.parse_args()
def get_envvars(env_file, ignore_not_found_error=False):
    """
    Set env vars from a file
    :param env_file:
    :param ignore_not_found_error: ignore not found error
    :return: list of tuples, env vars
    """
    env_vars = {}
    try:
        with open(env_file) as f:
            for line in f:
                line = line.replace('\n', '')
                if not line or line.startswith('#'):
                    continue
                try:
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
                except ValueError:
                    logging.error(
                        f"envar_utils.get_envvars error parsing line: '{line}'")
                    raise
    except FileNotFoundError:
        if not ignore_not_found_error:
            raise

    return env_vars

def create_config_file():
    # Remove telegraf.config before create a new file
    if os.path.exists(telegraf_config_file):
        os.remove(telegraf_config_file)
    else:
        print("The file does not exist!")

    # Create telegraf.config from template
    with open(telegraf_config_file_template, "r") as input:
        with open(telegraf_config_file, "w") as output:
            # Writing each line from input file to
            for line in input:
                output.write(line)
    
    replace_env_config()

def replace_env_config():
    with open(telegraf_config_file, 'r') as file:
        data = file.read()
        for key, value in get_envvars(args.env).items():
            data = data.replace('$'+key, value)
    
    with open(telegraf_config_file, 'w') as file:
        file.write(data)

def install_telegraf():
    # create a new config with new parameter.
    create_config_file()
    # start service telegraf
    # os.system(f'net start telegraf')

install_telegraf()