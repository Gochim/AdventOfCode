import math


# Task - https://adventofcode.com/2019/day/1
def main():
    data = open("day01_01.txt", 'r')
    final = 0
    for mass in data:
        fuel = math.trunc(int(mass) / 3) - 2
        final = final + fuel
    data.close()
    print(final)
    return


if __name__ == '__main__':
    main()