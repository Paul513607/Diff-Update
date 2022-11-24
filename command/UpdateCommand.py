import sys
import os
from command.Command import Command


class UpdateCommand(Command):
    def __init__(self, name, argv):
        super().__init__(name, argv)

    def check_valid(self):
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
        fd = open(diff_file, 'r')

        diff_lines = [line.rstrip() for line in fd.readlines()]
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
        print('UpdateCommand.execute() for argv: ' + str(self.argv))
        to_update_file = self.argv[0]
        to_update_file_name = os.path.basename(to_update_file)

        diff_file = self.argv[1]
        root = os.path.abspath(os.path.dirname(diff_file))
        diff_name = os.path.splitext(os.path.basename(diff_file))[0]
        latest_file_name = diff_name + '.latest'
        latest_file = os.path.join(root, latest_file_name + '1')

        ff = open(to_update_file, 'r')
        fl = open(latest_file, 'w')

        diff_data = self.get_diff_from_diff_file(diff_file, to_update_file_name, latest_file_name)
        diff_data.pop()
        to_update_file_lines = [line.rstrip() for line in ff.readlines()]

        i, j = 1, 0
        while i < len(diff_data) and j < len(to_update_file_lines):
            if diff_data[i].startswith('+'):
                fl.write(diff_data[i][1:] + '\n')
                i += 1
            elif diff_data[i].startswith('-'):
                i += 1
                j += 1
            else:
                fl.write(to_update_file_lines[j] + '\n')
                i += 1
                j += 1

        ff.close()
        fl.close()
