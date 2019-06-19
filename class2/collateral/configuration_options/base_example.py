import ipdb
from nornir import InitNornir


def main():
    nr = InitNornir()
    print(nr)
    ipdb.set_trace()


if __name__ == "__main__":
    main()
