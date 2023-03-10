#!/usr/bin/env python

import optparse
import os
import subprocess
import sys
import shutil
import logging

__FILES_DIRECTORY = 'files'
__GROUP_VARS_DIRECTORY = 'group_vars'
__HOST_VARS_DIRECTORY = 'host_vars'
__INVENTORY_DIRECTORY = 'inventories'
__ROLES_DIRECTORY = 'roles'

__DIRECTORIES_STRUCTURE = [__FILES_DIRECTORY,
                           __GROUP_VARS_DIRECTORY,
                           __HOST_VARS_DIRECTORY,
                           __INVENTORY_DIRECTORY,
                           __ROLES_DIRECTORY]

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

playbook_path = '..'
playbook_title = 'playbook'


def main():
    p = optparse.OptionParser(description='System utility for creating ansible playbooks file structure',
                              version='0.1',
                              prog='pyansible',
                              usage="%prog [--path <path to playbook> --name <name of the folder> --role <name of the "
                                    "role>]")
    init_options(p)
    options, arguments = p.parse_args()

    if options.path and options.name:
        path = os.path.join(options.path, options.name)
        if os.path.exists(path):
            response = input('The directory structure already exists, do you want to override it [Y]/N\n')
            if response == '' or response.lower() == 'y':
                shutil.rmtree(path)
            else:
                sys.exit(1)

        logging.info('Creating directory structure in path %s and with name %s' % (options.path, options.name))
        create_directory_structure(options.path, options.name)


def init_options(p):
    p.add_option("--path", "-p", action="store", dest="path", nargs=1)
    p.add_option("--name", "-n", action="store", dest="name", nargs=1)

    p.set_defaults(path='..', name=playbook_title)


def __create_playbook_yaml_file(name, extension='.yml'):
    __create_empty_file(name, extension)


def __create_empty_file(name, extension=''):
    with open(name + extension, 'w'):
        pass
    logging.info('Created file %s' % name)


def __create_ansible_role(path, role_name):
    os.chdir(path)
    subprocess.call('ansible-galaxy role init %s' % role_name, shell=True)


def create_directory_structure(path, name):
    fullpath = os.path.join(path, name)
    os.mkdir(fullpath)

    for directory in __DIRECTORIES_STRUCTURE:
        os.mkdir(os.path.join(fullpath, directory))

    for directory, directories, filename in os.walk(fullpath):
        logging.info('Entering directory %s' % directory)
        if os.path.basename(directory) in [__HOST_VARS_DIRECTORY, __INVENTORY_DIRECTORY, __GROUP_VARS_DIRECTORY]:
            logging.info('Creating structure for basename in %s' % os.path.basename(directory))
            response = input('Do you want to create configuration file per environment? [Y]/N\n')
            if response == '' or response.lower() == 'y':
                response = input('Enter the environment files names separated by a ","?\n')
                for env in response.split(','):
                    __create_empty_file(os.path.join(str(os.path.abspath(directory)), str(env)))
            else:
                continue

    __create_playbook_yaml_file(os.path.join(fullpath, name))
    __create_empty_file(os.path.join(fullpath, 'requirements'), '.txt')
    __create_ansible_role(os.path.join(fullpath, 'roles'), 'common')


if __name__ == "__main__":
    main()
