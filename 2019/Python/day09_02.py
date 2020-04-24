from file_utils import read_data_to_array

PARAMETER_MODE_POSITION = 0
PARAMETER_MODE_VALUE = 1
PARAMETER_MODE_RELATIVE = 2

COMMAND_HALT = 99
COMMAND_INPUT = 3
COMMAND_OUTPUT = 4


# Task - https://adventofcode.com/2019/day/9
def main():
    starting_data = read_data_to_array("day09.txt")
    expected_output = None

    # Tests
    # starting_data = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    # starting_data = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    # starting_data = [104, 1125899906842624, 99]

    cur_value = 2
    return_code = 0

    amplifier = Amplifier(starting_data)
    while return_code != COMMAND_HALT:
        return_code, cur_value = amplifier.run_amplifier(cur_value)


class Amplifier:
    def __init__(self, starting_data, phase_setting=None) -> None:
        self._phase_setting = phase_setting
        self._phase_setting_set = phase_setting is None
        self._starting_program = starting_data.copy()
        self._ipr = IntCodeProgram(starting_data.copy())
        self._output_params = [0]
        self._input_value = self._index = self._steps = 0

        self._command_map = {
            1: self.command_add,
            2: self.command_mlt,
            3: self.command_input,
            4: self.command_output,
            5: self.command_jump_if_true,
            6: self.command_jump_if_false,
            7: self.command_less_than,
            8: self.command_equals,
            9: self.command_rel_base_offset,
            99: self.command_halt
        }

    def run_amplifier(self, input_value):
        self._input_value = input_value
        exit_op, output = self.execute_program()
        return exit_op, output

    def execute_program(self):
        try:
            while True:
                com_params = self._ipr.decode_command_params()
                func = self._command_map.get(com_params[0])
                self._ipr.index = func(com_params)
                self._steps += 1

                if com_params[0] in [COMMAND_HALT, COMMAND_OUTPUT]:
                    break
        except:
            print(" == Raised error on step {} with command {}".format(self._steps, com_params))
            exit(252)

        # noinspection PyUnboundLocalVariable
        return com_params[0], self._output_params[0]

    def _prepare_input_value(self):
        input_value = self._input_value if self._phase_setting_set else self._phase_setting
        self._phase_setting_set = True
        return input_value

    def command_add(self, com_params):
        first = self._ipr.get_data(1, com_params[1])
        second = self._ipr.get_data(2, com_params[2])
        self._ipr.set_data(3, com_params[3], first + second)
        return self._ipr.index + 4

    def command_mlt(self, com_params):
        first = self._ipr.get_data(1, com_params[1])
        second = self._ipr.get_data(2, com_params[2])
        self._ipr.set_data(3, com_params[3], first * second)
        return self._ipr.index + 4

    def command_input(self, com_params):
        self._ipr.set_data(1, com_params[1], self._prepare_input_value())
        return self._ipr.index + 2

    def command_output(self, com_params):
        diag_code = self._ipr.get_data(1, com_params[1])
        print("{} after {} steps".format(diag_code, self._steps))
        self._output_params = [diag_code]
        return self._ipr.index + 2

    def command_jump_if_true(self, com_params):
        if self._ipr.get_data(self._index + 1, com_params[1]) > 0:
            result = self._ipr.get_data(self._index + 2, com_params[2])
        else:
            result = self._ipr.index + 3
        return result

    def command_jump_if_false(self, com_params):
        if self._ipr.get_data(self._index + 1, com_params[1]) == 0:
            result = self._ipr.get_data(self._index + 2, com_params[2])
        else:
            result = self._ipr.index + 3
        return result

    def command_less_than(self, com_params):
        if self._ipr.get_data(1, com_params[1]) < self._ipr.get_data(2, com_params[2]):
            self._ipr.set_data(3, com_params[3], 1)
        else:
            self._ipr.set_data(3, com_params[3], 0)
        return self._ipr.index + 4

    def command_equals(self, com_params):
        if self._ipr.get_data(1, com_params[1]) == self._ipr.get_data(2, com_params[2]):
            self._ipr.set_data(3, com_params[3], 1)
        else:
            self._ipr.set_data(3, com_params[3], 0)
        return self._ipr.index + 4

    def command_rel_base_offset(self, com_params):
        self._ipr.set_rel_base_offset(self._ipr.get_data(1, com_params[1]))
        return self._ipr.index + 2

    def command_halt(self, com_params):
        return self._ipr.index

    def command_(self, com_params):
        pass


class IntCodeProgram:
    def __init__(self, program) -> None:
        self._program = self._prepare_data(program)
        self._relative_base = 0
        self.index = 0

    def get_data(self, shift, param_mode):
        adj_index = self._get_index(self._program, self.index + shift, param_mode)
        result = self._program.get(adj_index) if self._program.get(adj_index) is not None else 0
        return result

    def set_data(self, shift, param_mode, value):
        adj_index = self._get_index(self._program, self.index + shift, param_mode)
        self._program[adj_index] = value

    def set_rel_base_offset(self, offset):
        self._relative_base += offset

    def decode_command_params(self):
        code = self._program[self.index]
        command = code % 100
        code //= 100
        param_mode_1 = code % 10
        code //= 10
        param_mode_2 = code % 10
        code //= 10
        param_mode_3 = code % 10
        code //= 10

        return command, param_mode_1, param_mode_2, param_mode_3

    def _prepare_data(self, data):
        result = {}
        for index, item in enumerate(data):
            result[index] = item

        return result

    def _get_index(self, input_data, index, param_mode):
        if param_mode is PARAMETER_MODE_POSITION:
            adj_index = input_data[index]
        elif param_mode is PARAMETER_MODE_VALUE:
            adj_index = index
        elif param_mode is PARAMETER_MODE_RELATIVE:
            adj_index = self._relative_base + input_data[index]
        else:
            raise ValueError("Wrong mode parameter {}".format(param_mode))

        return adj_index


if __name__ == '__main__':
    main()
