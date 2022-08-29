from itertools import permutations, islice


def find_milionth_permutation(numbers: list):
    perm = islice(permutations(numbers), 999999, None)
    milionth = next(perm)
    result = "".join(str(num) for num in milionth)
    return result


def main():
    perm_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = find_milionth_permutation(perm_numbers)
    #print(result)


if __name__ == "__main__":
    for i in range(20):
        main()
