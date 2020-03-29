class Command:
    def __init__(self, code, length) -> None:
        self.code = code
        self.length = length

    def execute(self):
        raise ValueError("No command initialized")


class CommandHalt(Command):
    def __init__(self) -> None:
        super().__init__(99, 1)

    def execute(self):
        pass


class CommandAdd(Command):
    def __init__(self) -> None:
        super().__init__(1, 1)

    def execute(self):
        pass


# Task - https://adventofcode.com/2019/day/7
def main():

    return


if __name__ == '__main__':
    main()
