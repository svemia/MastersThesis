import sys


def make_pi(precision: int):
    q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
    for j in range(precision):
        if 4 * q + r - t < m * t:
            yield m
            q, r, t, k, m, x = 10*q, 10*(r-m*t), t, k, (10*(3*q+r))//t - 10*m, x
        else:
            q, r, t, k, m, x = q*k, (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2


def main(pi_size: int):
    pi_list = []
    for i in make_pi(pi_size):
        pi_list.append(str(i))

    pi_list = pi_list[:1] + ['.'] + pi_list[1:]
    pi_string = "".join(pi_list)
    #print(pi_string)


if __name__ == '__main__':
    pi_size = int(sys.argv[1])
    # main()
    for i in range(20):
        main(pi_size)
