import sys
import os
from command.Command import Command
from diff.Differ import Differ


class CreateCommand(Command):
    def __init__(self, name, argv):
        super().__init__(name, argv)

    def check_valid(self):
        if len(self.argv) < 2:
            print('Usage: python diff-update.py create <main_file> [match_files]')
            sys.exit(1)
        if not os.path.exists(self.argv[0]):
            print('Latest file not found: ' + self.argv[0])
            sys.exit(1)
        for i in range(1, len(self.argv)):
            if not os.path.exists(self.argv[i]):
                print('Version file not found: ' + self.argv[i])
                sys.exit(1)

    def execute(self):
        print('CreateCommand.execute() for argv: ' + str(self.argv))
        latest_file = self.argv[0]
        root = os.path.abspath(os.path.dirname(latest_file))
        diff_file = os.path.splitext(os.path.basename(latest_file))[0] + '.diff'
        version_files = self.argv[1:]

        full_diff_path = os.path.join(root, diff_file)
        with open(full_diff_path, "w") as f:
            for i in range(0, len(version_files)):
                f.write("diff " + version_files[i] + " " + latest_file + ":\n")
                differ = Differ(version_files[i], latest_file)
                differ.fill_sequence_matrix()
                differ.reconstruct_path()
                differ.format_diff()
                for line in differ.diff:
                    f.write(line + '\n')
                f.write('\n')
