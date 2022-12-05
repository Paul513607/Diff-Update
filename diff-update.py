import sys
from command.CreateCommand import CreateCommand
from command.UpdateCommand import UpdateCommand

command = None

def init():
    """This function initializes the data"""
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
    command.check_valid()
    command.execute()


if __name__ == '__main__':
    init()
    run()
