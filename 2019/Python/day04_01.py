def check_cond(number):
    digits = []
    for i in range(6):
        digits.insert(0, number % 10)
        number //= 10

    double = False
    rising = True
    for index in range(1, len(digits)):
        if digits[index] == digits[index-1]:
            double = True
        if digits[index] < digits[index-1]:
            rising = False
            break

    return double and rising


def main():
    # print(check_cond(776621)) # False
    # print(check_cond(111111)) # True
    # print(check_cond(223450)) # False
    # print(check_cond(123789)) # False

    count = 0
    for item in range(278384, 824796):
        if check_cond(item):
            count += 1

    print(count)


if __name__ == '__main__':
    main()
