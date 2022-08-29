from math import floor, sqrt


def calculate_prime(number):
    for i in range(3, floor(sqrt(number)) + 1):
        if number % i == 0:
            return i
    return number


def find_smallest_prime(number):
    result = number

    while True:
        prime = calculate_prime(result)
        if prime < result:
            result //= prime
        else:
            return result


def main():
    number = 600851475143

    result = find_smallest_prime(number)
    print(str(result))


if __name__ == "__main__":
    # main()
    for i in range(20):
        main()
