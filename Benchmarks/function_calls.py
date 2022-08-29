def first_function(i: int):
    suma = 0
    for j in range(10):
        suma += second_function(i, j)
    return suma


def second_function(i: int, j:int):
    suma = 0
    for k in range(10):
        suma += third_function(i, j, k)
    return suma


def third_function(i:int, j:int, k:int):
    suma = 0
    if i % 10 == 0:
        suma += j
    else:
        suma += k
    return suma


def main():
    suma = 0
    for i in range(100000):
        suma += first_function(i)

    print(suma)


if __name__ == "__main__":
    # main()
    for i in range(20):
        main()