import sys


def fibonacci_recursion(number: int):
    if number <= 1:
        return number
    else:
        return fibonacci_recursion(number-1) + fibonacci_recursion(number-2)
    pass


def main(threshold: int):
    fibonacci_seq = []
    for number in range(threshold):
        fibonacci_seq.append(fibonacci_recursion(number))

    print(",".join(str(n) for n in fibonacci_seq))


if __name__ == "__main__":
    threshold = int(sys.argv[1])
    # main(size)
    for i in range(20):
        main(threshold)
