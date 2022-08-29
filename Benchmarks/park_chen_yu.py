from itertools import combinations
import sys
from math import floor

baskets = {}
item_counter = {}
couples = {}
cases = []
size = 0

"""Third passage of PYC algorithm."""


def third_passage(b, threshold):
    global baskets, item_counter, couples, cases
    for basket in baskets:
        for pair in combinations(baskets[basket], 2):
            if item_counter[pair[0]] >= threshold and item_counter[pair[1]] >= threshold:
                k = (pair[0] * size + pair[1]) % b
                if cases[k] >= threshold:
                    if pair not in couples:
                        couples[pair] = 1
                    else:
                        couples[pair] += 1


"""Second passage of PYC algorithm."""


def second_passage(b, threshold):
    global cases, baskets, item_counter, size
    cases = [0] * b

    for basket in baskets:
        for pair in combinations(baskets[basket], 2):
            if item_counter[pair[0]] >= threshold and item_counter[pair[1]] >= threshold:
                k = (pair[0] * size + pair[1]) % b
                cases[k] += 1


"""First passage of PYC algorithm."""


def first_passage(N):
    global baskets, item_counter
    for i in range(N):
        items = baskets[i]
        for item in items:
            if item not in item_counter:
                item_counter[item] = 1
            else:
                item_counter[item] += 1


"""Load baskets."""


def load_baskets(reader, N):
    global baskets
    for i in range(N):
        items = [int(item) for item in reader.readline().split(" ")]
        baskets[i] = items


"""Find frequent items."""


def find_frequent(threshold):
    m = 0
    for item in item_counter:
        if item_counter[item] >= threshold:
            m += 1
    return m * (m - 1) * 0.5


"""Start of execution."""


def main():
    global size, couples
    print("test")
    # reader = sys.stdin
    reader = open("/home/mia/Desktop/R.in", "r")
    N = int(reader.readline())
    s = float(reader.readline())
    b = int(reader.readline())

    threshold = floor(s * N)

    load_baskets(reader, N)
    first_passage(N)
    size = len(item_counter)
    second_passage(b, threshold)
    third_passage(b, threshold)

    # sys.stdout.write(str(int(find_frequent(threshold))) + '\n')
    # sys.stdout.write(str(len(couples)) + '\n')
    # for result in sorted(couples.values(), reverse=True):
    #    sys.stdout.write(str(result) + '\n')


"""Script entry point."""
if __name__ == '__main__':
    # main()
    for i in range(20):
        main()
