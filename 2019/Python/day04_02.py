def check_cond(number):
    digits = []
    for i in range(6):
        digits.insert(0, number % 10)
        number //= 10

    double = False
    rising = True
    index = 0
    while index < len(digits) - 1:
        if digits[index] > digits[index + 1]:
            rising = False
            break

        if digits[index] == digits[index + 1]:
            inner_index = index + 1
            while (inner_index <= 4) and digits[inner_index] == digits[inner_index + 1]:
                inner_index += 1

            if inner_index - index == 1:
                double = True
            index = inner_index
        else:
            index += 1

    return double and rising


def main():
    # print(check_cond(278888)) # False
    # print(check_cond(788013)) # False

    count = 0
    for item in range(278384, 824796):
        if check_cond(item):
            count += 1

    print(count)


if __name__ == '__main__':
    main()
