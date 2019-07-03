from nornir import InitNornir


def main():
    nr = InitNornir()
    for host in nr.inventory.hosts:
        print(nr.inventory.hosts[host]["timezone"])
    print(nr.inventory.hosts["arista3"].data)
    print(nr.inventory.hosts["arista3"].items())
    print(nr.inventory.hosts["arista3"]["timezone"])


if __name__ == "__main__":
    main()
