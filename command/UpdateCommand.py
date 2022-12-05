import sys
import os
from command.Command import Command

"""
UpdateCommand class
For updating the latest file with the diff file
Child of the generic Command class
"""
class UpdateCommand(Command):
    def __init__(self, name, argv):
        super().__init__(name, argv)

    def check_valid(self):
        """Overridden method for checking if the arguments are valid"""
        if len(self.argv) < 2:
            print('Usage: python diff-update.py update <to_update_file> <diff_file>')
            sys.exit(1)
        if not os.path.exists(self.argv[0]):
            print('File to update not found: ' + self.argv[0])
            sys.exit(1)
        if not os.path.exists(self.argv[1]):
            print('Diff file not found: ' + self.argv[1])
            sys.exit(1)

    def get_diff_from_diff_file(self, diff_file, to_update_file_name, latest_file_name):
        """
            This method is used to get the diff data for the current version file (if it is available)
            :param diff_file: The path to the diff file
            :param to_update_file_name: The name of the file that we want to update
            :param latest_file_name: The name of the latest file
        """
        fd = open(diff_file, 'rb')

        diff_lines = [line.rstrip().decode('utf-8') for line in fd.readlines()]
        diff_starts = [(i, line) for i, line in enumerate(diff_lines) if line.startswith('diff')]
        diff_for_update, diff_for_update_idx = None, None
        for idx in range(0, len(diff_starts)):
            if to_update_file_name in diff_starts[idx][1] and latest_file_name in diff_starts[idx][1]:
                diff_for_update = diff_starts[idx][0]
                diff_for_update_idx = idx
                break
        if diff_for_update is None or diff_for_update_idx is None:
            fd.close()
            raise Exception('No diff found for file: ' + to_update_file_name)

        fd.close()
        if diff_for_update_idx < len(diff_starts) - 1:
            return diff_lines[diff_for_update:diff_starts[diff_for_update_idx + 1][0]]
        else:
            return diff_lines[diff_for_update:]

    def execute(self):
        """Overridden method for applying the command's logic
        This method uses the data from the diff file for the current version file, and creates the latest file
        using the version file and the updates from the diff file associated with it"""
        print('UpdateCommand.execute() for argv: ' + str(self.argv))
        to_update_file = self.argv[0]
        to_update_file_name = os.path.basename(to_update_file)

        diff_file = self.argv[1]
        root = os.path.abspath(os.path.dirname(diff_file))
        diff_name = os.path.splitext(os.path.basename(diff_file))[0]
        latest_file_name = diff_name + '.latest'
        latest_file = os.path.join(root, latest_file_name + '1')

        ff = open(to_update_file, 'rb')
        fl = open(latest_file, 'wb')

        diff_data = self.get_diff_from_diff_file(diff_file, to_update_file_name, latest_file_name)
        diff_data.pop()
        to_update_file_lines = [line.rstrip().decode('utf-8') for line in ff.readlines()]

        i, j = 1, 0
        while i < len(diff_data) and j < len(to_update_file_lines):
            if diff_data[i].startswith('+'):
                fl.write(str.encode(diff_data[i][1:] + '\n'))
                i += 1
            elif diff_data[i].startswith('-'):
                i += 1
                j += 1
            else:
                fl.write(str.encode(to_update_file_lines[j] + '\n'))
                i += 1
                j += 1

        ff.close()
        fl.close()
