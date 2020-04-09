import itertools


def read_data_to_array(data_file):
    data = open(data_file, 'r')
    result = [int(x) for x in data.readline().split(",")]
    data.close()

    return result


PARAMETER_MODE_POSITION = 0
PARAMETER_MODE_VALUE = 1

COMMAND_HALT = 99


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
    result = get_data(input_data, index + 1, com_params[1]) + get_data(input_data, index + 2, com_params[2])
    input_data[input_data[index + 3]] = result
    return index + 4


def command_mlt(input_data, index, com_params, adt_params):
    first = get_data(input_data, index + 1, com_params[1])
    second = get_data(input_data, index + 2, com_params[2])
    result = first * second
    input_data[input_data[index + 3]] = result
    return index + 4


def command_input(input_data, index, com_params, adt_params):
    input_data[input_data[index + 1]] = input_params.pop(0)
    return index + 2


def command_output(input_data, index, com_params, adt_params):
    diag_code = get_data(input_data, index + 1, com_params[1])
    output_params.append(diag_code)
    print("{} after {} steps".format(diag_code, adt_params))
    return index + 2


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


def command_(input_data, index, com_params):
    pass


input_params = []
output_params = []

command_map = {
    1: command_add,
    2: command_mlt,
    3: command_input,
    4: command_output,
    5: command_jump_if_true,
    6: command_jump_if_false,
    7: command_less_than,
    8: command_equals
}


def execute_program(program):
    index, steps = 0, 0
    try:
        while decode_command_params(program[index])[0] is not COMMAND_HALT:
            com_params = decode_command_params(program[index])

            func = command_map.get(com_params[0])
            if func is None:
                raise ValueError("Unknown command")
            else:
                index = func(program, index, com_params, (steps))

            steps += 1
    except:
        print(" == Raised error on step {}".format(steps))


    print("{} total steps".format(steps))


def run_amplifier(starting_data, phase_setting, input_value):
    global input_params
    global output_params
    output_params.clear()
    program = starting_data.copy()
    input_params = [phase_setting, input_value]
    execute_program(program)
    return output_params[0]


# Task - https://adventofcode.com/2019/day/7
def main():
    starting_data = read_data_to_array("day07.txt")
    expected_output = None
    # starting_data = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    # expected_output = 43210
    # starting_data = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    # expected_output = 54321
    # starting_data = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
    #                  1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    # expected_output = 65210

    phase_settings = [0, 1, 2, 3, 4]
    max_value = 0
    max_settings = []
    for subset in itertools.permutations(phase_settings, len(phase_settings)):
        cur_value = run_amplifier(starting_data, subset[0], 0)
        cur_value = run_amplifier(starting_data, subset[1], cur_value)
        cur_value = run_amplifier(starting_data, subset[2], cur_value)
        cur_value = run_amplifier(starting_data, subset[3], cur_value)
        cur_value = run_amplifier(starting_data, subset[4], cur_value)

        if cur_value > max_value:
            max_value = cur_value
            max_settings = subset

    if expected_output is not None:
        print("=== Output is correct {}".format(max_value)) if expected_output == max_value else \
            print("Received {} instead of {}".format(expected_output, max_value))
    print(max_value)
    print(max_settings)


if __name__ == '__main__':
    main()
