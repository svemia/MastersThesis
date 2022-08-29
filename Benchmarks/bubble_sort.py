import sys
from random import randint


def bubble_sort(list_to_sort: list):
    length = len(list_to_sort)

    for i in range(length-1):
        for j in range(0, length-i-1):
            if list_to_sort[j] > list_to_sort[j+1]:
                list_to_sort[j], list_to_sort[j+1] = list_to_sort[j+1], list_to_sort[j]

    return list_to_sort


def main():
    print("test")
    list_to_sort = []
    size = int(sys.argv[1])
    rand_range = size + 10000
    for i in range(0, size):
        list_to_sort.append(randint(0, rand_range))

    result = bubble_sort(list_to_sort)
    #print(", ".join(str(num) for num in result))


if __name__ == "__main__":
    for i in range(20):
        main()

    #main()