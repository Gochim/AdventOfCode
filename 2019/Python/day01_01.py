import math


# Task - https://adventofcode.com/2019/day/1
def main():
    data = open("day01_01.txt", 'r')
    fuels = [(math.trunc(int(mass) / 3) - 2) for mass in data]
    final = sum(fuels)
    data.close()
    print(final)


if __name__ == '__main__':
    main()