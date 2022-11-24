from abc import abstractmethod


class Command:
    name: str
    argv: list

    def __init__(self, name: str, argv: list):
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
