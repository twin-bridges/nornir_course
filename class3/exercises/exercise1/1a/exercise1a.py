from nornir import InitNornir


def main():
    nr = InitNornir()
    print(nr.inventory.hosts["arista3"].data)
    print(nr.inventory.hosts["arista3"].items())


if __name__ == "__main__":
    main()
