#!/usr/bin/env python

import optparse
import os
import subprocess
import sys
import shutil
import logging

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

playbook_path = '.'
playbook_title = 'playbook'

def main():
    p = optparse.OptionParser(description='System utility for creating ansible playbooks file structure',
                              version='0.1',
                              prog='pyansible',
                              usage="%prog [--path <path to plabook> --name <name of the folder> --role <name of the role>]")
    p.add_option("--path", "-p", action="store", dest="path", nargs=1)
    p.add_option("--name", "-n", action="store", dest="name", nargs=1)
    
    p.set_defaults(path='.', name='myplaybook')
    options, arguments = p.parse_args()
    
    if options.path and options.name:
        if os.path.exists(os.path.join(options.path, options.name)):
            response = input('The directory structure already exists, do you want to override it [Y]/N\n')
            if response == 'Y':
                shutil.rmtree(os.path.join(options.path, options.name))
            else:
                sys.exit(1)
                
        logging.info('Creating directory structure in path %s and with name %s' % (options.path, options.name))
        create_directory_structure(options.path, options.name)

def create_playbook_yaml_file(name):
    with open(name + '.yml', 'w'):
        pass
    logging.info('Created file %s' % name)

def create_ansible_role(path, role_name):
    os.chdir(path)
    subprocess.call('ansible-galaxy role init %s' % role_name, shell=True)

def create_directory_structure(path, name):
    fullpath = os.path.join(path, name)
    os.mkdir(fullpath) 

    environmentdir = ['dev', 'uat', 'prd']

    for dir in ['files', 'group_vars', 'host_vars', 'inventories', 'roles']:
        os.mkdir(os.path.join(fullpath, dir))
    
    for dir, dirs, filename in os.walk(fullpath):
        logging.info('Entring directory %s' % dir)
        if os.path.basename(dir) == 'host_vars' or os.path.basename(dir) == 'inventories':
            logging.info('Creating structure for basename in %s' % os.path.basename(dir))
            for env in environmentdir:
                os.mkdir(os.path.join(os.path.abspath(dir), env))
        if os.path.basename(dir) == 'inventories':
            for env in environmentdir:
                with open('dev', 'w'):
                    pass
    
    create_playbook_yaml_file(os.path.join(fullpath,name))
    create_ansible_role(os.path.join(fullpath, 'roles'), 'common')


if __name__ == "__main__":
    main()  
