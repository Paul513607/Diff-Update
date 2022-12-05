from abc import abstractmethod, ABC

"""
Command is an abstract class that defines the interface for all commands.
"""
class Command(ABC):
    name: str
    argv: list

    def __init__(self, name: str, argv: list):
        """
        :param name: The name of the latest file (create) or the file we want to update (update)
        :param argv: The other files to diff (create) or the diff file (update)
        """
        self.name = name
        self.argv = argv

    def __str__(self):
        return f'Command({self.name}, {self.argv})'

    @abstractmethod
    def check_valid(self):
        pass

    @abstractmethod
    def execute(self):
        pass
