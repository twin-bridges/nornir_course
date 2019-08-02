from nornir import InitNornir


def main():
    nr = InitNornir()
    print()
    print(nr.inventory.hosts["arista3"].data)
    # Cast as a dict() to make output more readable
    print(dict(nr.inventory.hosts["arista3"].items()))
    print()


if __name__ == "__main__":
    main()
