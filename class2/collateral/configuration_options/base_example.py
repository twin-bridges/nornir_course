"""This code will fail due to missing hosts.yaml file."""
import pdbr
from nornir import InitNornir


def main():
    nr = InitNornir()
    print(nr)
    pdbr.set_trace()


if __name__ == "__main__":
    main()
