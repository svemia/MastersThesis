def find_triplets(number: int):
    for first in range(1, number + 1):
        for second in range(first + 1, number + 1):
            third = number - first - second
            if pow(first, 2) + pow(second, 2) == pow(third, 2):
                return first, second, third


def main():
    equals = 1000
    first, second, third = find_triplets(equals)

    print("{}, {}, {}".format(first, second, third))


if __name__ == "__main__":
    # main()
    for i in range(20):
        main()
