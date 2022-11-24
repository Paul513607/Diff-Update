import sys
from command.CreateCommand import CreateCommand
from command.UpdateCommand import UpdateCommand
from diff.Differ import Differ
import difflib

command = None


def init():
    global command
    if len(sys.argv) < 3:
        print('Usage: python diff-update.py <command> <main_file> [match_files]')
        sys.exit(1)
    command_name = sys.argv[1]
    if command_name == 'create':
        command = CreateCommand(command_name, sys.argv[2:])
    elif command_name == 'update':
        command = UpdateCommand(command_name, sys.argv[2:])
    else:
        print('Unknown command: ' + command_name)
        sys.exit(1)


def run():
    init()
    command.check_valid()
    command.execute()


if __name__ == '__main__':
    run()
    #differ = Differ("./data/a2.latest", "./data/a2.ver1")
    #diff = difflib.unified_diff(differ.file1_lines, differ.file2_lines)
    #print(''.join(diff))
