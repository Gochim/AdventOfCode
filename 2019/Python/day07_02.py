from itertools import permutations
from file_utils import read_data_to_array

PARAMETER_MODE_POSITION = 0
PARAMETER_MODE_VALUE = 1

COMMAND_HALT = 99
COMMAND_INPUT = 3
COMMAND_OUTPUT = 4


def decode_command_params(code):
    command = code % 100
    code //= 100

    param_mode_1 = code % 10
    code //= 10

    param_mode_2 = code % 10
    code //= 10

    param_mode_3 = code % 10
    code //= 10

    return command, param_mode_1, param_mode_2, param_mode_3


def get_data(input_data, index, param_mode):
    result = 0
    if param_mode is PARAMETER_MODE_POSITION:
        result = input_data[input_data[index]]
    elif param_mode is PARAMETER_MODE_VALUE:
        result = input_data[index]

    return result


def command_add(input_data, index, com_params, adt_params):
    first = get_data(input_data, index + 1, com_params[1])
    second = get_data(input_data, index + 2, com_params[2])
    input_data[input_data[index + 3]] = first + second
    return index + 4


def command_mlt(input_data, index, com_params, adt_params):
    first = get_data(input_data, index + 1, com_params[1])
    second = get_data(input_data, index + 2, com_params[2])
    input_data[input_data[index + 3]] = first * second
    return index + 4


def command_input(input_data, index, com_params, adt_params):
    input_data[input_data[index + 1]] = adt_params
    return index + 2


def command_output(input_data, index, com_params, adt_params):
    diag_code = get_data(input_data, index + 1, com_params[1])
    print("{} after {} steps".format(diag_code, adt_params))
    return index + 2, diag_code


def command_jump_if_true(input_data, index, com_params, adt_params):
    if get_data(input_data, index + 1, com_params[1]) > 0:
        result = get_data(input_data, index + 2, com_params[2])
    else:
        result = index + 3
    return result


def command_jump_if_false(input_data, index, com_params, adt_params):
    if get_data(input_data, index + 1, com_params[1]) == 0:
        result = get_data(input_data, index + 2, com_params[2])
    else:
        result = index + 3
    return result


def command_less_than(input_data, index, com_params, adt_params):
    if get_data(input_data, index + 1, com_params[1]) < get_data(input_data, index + 2, com_params[2]):
        input_data[input_data[index + 3]] = 1
    else:
        input_data[input_data[index + 3]] = 0
    return index + 4


def command_equals(input_data, index, com_params, adt_params):
    if get_data(input_data, index + 1, com_params[1]) == get_data(input_data, index + 2, com_params[2]):
        input_data[input_data[index + 3]] = 1
    else:
        input_data[input_data[index + 3]] = 0
    return index + 4


def command_halt(self, input_data, index, com_params):
    return index


def command_(self, input_data, index, com_params):
    pass


class Amplifier:
    def __init__(self, starting_data, phase_setting) -> None:
        self._phase_setting = phase_setting
        self._phase_setting_set = False
        self._program = starting_data.copy()
        self._output_params = [0]
        self._input_value = self._index = self._steps = 0

        self._command_map = {
            1: command_add,
            2: command_mlt,
            3: command_input,
            4: command_output,
            5: command_jump_if_true,
            6: command_jump_if_false,
            7: command_less_than,
            8: command_equals,
            99: command_halt
        }

    def run_amplifier(self, input_value):
        self._input_value = input_value
        exit_op, output = self.execute_program()
        return exit_op, output

    def execute_program(self):
        try:
            while True:
                com_params = decode_command_params(self._program[self._index])

                func = self._command_map.get(com_params[0])
                if com_params[0] is COMMAND_INPUT:
                    self._index = func(self._program, self._index, com_params, self._prepare_input_value())
                elif com_params[0] is COMMAND_OUTPUT:
                    (self._index, data) = func(self._program, self._index, com_params, self._steps)
                    self._output_params = [data]
                else:
                    self._index = func(self._program, self._index, com_params, self._steps)

                self._steps += 1

                if com_params[0] in [COMMAND_HALT, COMMAND_OUTPUT]:
                    break
        except:
            print(" == Raised error on step {}".format(self._steps))

        # noinspection PyUnboundLocalVariable
        return com_params[0], self._output_params[0]

    def _prepare_input_value(self):
        input_value = self._input_value if self._phase_setting_set else self._phase_setting
        self._phase_setting_set = True
        return input_value


# Task - https://adventofcode.com/2019/day/7
def main():
    starting_data = read_data_to_array("day07.txt")
    expected_output = None

    # Tests
    # starting_data = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
    #                  27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
    # expected_output = 139629729

    # starting_data = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
    #                  -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
    #                  53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
    # expected_output = 18216

    phase_settings = [5, 6, 7, 8, 9]
    amp_count = len(phase_settings)

    max_value = 0
    for phase_settings in permutations(phase_settings, amp_count):
        cur_value = return_code = 0
        amplifiers = [Amplifier(starting_data, phase_settings[i]) for i in range(amp_count)]

        while return_code != COMMAND_HALT:
            for i in range(amp_count):
                return_code, cur_value = amplifiers[i].run_amplifier(cur_value)

        max_value = max(cur_value, max_value)

    print(max_value)

    if expected_output is not None:
        print("=== Output is correct {}".format(max_value)) if expected_output == max_value else \
            print("Received {} instead of {}".format(max_value, expected_output))


if __name__ == '__main__':
    main()
