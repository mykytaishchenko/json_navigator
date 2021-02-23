"""Docs"""

import json
import os


dir_name_len = 10


def read(file_name: str):
    """
    This function opens json file.
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        json_file = json.load(file)
    return json_file


def show_files(curr_directory, command):
    """
    This function shows folders (lists, dicts, etc.)
    """
    print('Directory objects:')

    folders = []
    if type(curr_directory) == list:
        for element in curr_directory:
            if type(element) is dict or type(element) is list:
                folders.append(element)
                print(f"-- {str(type(element))[8:-2]} {str(len(folders))} ({str(element)[:dir_name_len]}...)")
            else:
                print("-- " + str(element))

    elif type(curr_directory) == dict:
        for element in curr_directory.keys():
            print("-- " + str(element))

    else:
        print(f'{command}: {curr_directory}')

    return folders


def cmd(folders, path, prev_command):
    """
    Function was made to work with user's inputs.
    """

    global dir_name_len

    curr_directory = path[-1]
    command = input('Command: ')

    comments = ''
    if len(command) > 1 and command.split()[0] == 'cmd':
        if command == "cmd back":
            if len(path) > 1:
                path.pop()
            else:
                comments = 'It`s root directory.'
        elif command == "cmd exit":
            exit(0)
        elif command.startswith("cmd dir_name_len"):
            if len(command.split()) > 2 and command.split()[2].isdigit():
                dir_name_len = int(command.split()[2])
            else:
                comments = 'Incorrect length.'
        else:
            comments = 'No such command.'

    elif type(curr_directory) in [list, dict]:
        if command in curr_directory:
            path.append(curr_directory[command])
        elif len(command.split()) == 2 and command.split()[0] in ['list', 'dict'] \
                and 0 < int(command.split()[1]) <= len(folders):
            path.append(curr_directory[int(command.split()[1]) - 1])
        else:
            comments = 'No such object.'

    else:
        comments = 'This is the value of the object, there are no nested objects in it.'
        command = prev_command

    return path, comments, command


def show_instruction():
    """
    This function prints instructions.
    """
    print('To open an object or get the value of a parameter, enter its name.')
    print('If you want to go back enter "cmd back".')
    print('If you want to end session enter "cmd exit".\n')


def navigator(file):
    """
    This function does all moves by levels on a .json file.
    """
    path = [file]
    comments = ''
    command = ''

    while 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_instruction()

        folders = show_files(path[-1], command)
        print(f'\n{comments}' if comments != '' else '')

        path, comments, command = cmd(folders, path, command)


def user_input():
    """
    This function checks whether the file exits.
    If yes - it works with it.
    """

    while 1:
        file_path = input('Enter the path to the json file you want to open: ')
        if not file_path.endswith('.json'):
            print('It`s not json file.')
        elif not os.path.isfile(file_path):
            print('No such file.')
        else:
            break

        if input('Try again?[y/n]: ') not in ['y', 'Y']:
            return 0
    navigator(read(file_path))


user_input()
