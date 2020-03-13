import math


def positive(value):
    return 0 if value < 0 else value


def main():
    data = open("day01_01.txt", 'r')
    final = 0
    for mass in data:
        module_fuel = 0
        iteration_fuel = mass
        while True:
            iteration_fuel = positive(math.trunc(int(iteration_fuel) / 3) - 2)
            module_fuel = module_fuel + iteration_fuel
            if iteration_fuel == 0:
                break

        final = final + module_fuel

    data.close()
    print(final)
    return


if __name__ == '__main__':
    main()
