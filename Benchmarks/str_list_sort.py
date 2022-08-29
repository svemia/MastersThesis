import sys
from random import choices, randint
from string import ascii_lowercase, ascii_uppercase, digits


def main(list_size: int):
    pool = ascii_lowercase + ascii_uppercase + digits
    list_strings = []

    for i in range(list_size):
        str_size = randint(1, 100)
        list_strings.append("".join((choices(pool, k=str_size))))

    list_strings.sort(key=len)
    #print(list_strings)


if __name__ == "__main__":
    list_size = int(sys.argv[1])
    #main(list_size)
    for i in range(20):
        main(list_size)