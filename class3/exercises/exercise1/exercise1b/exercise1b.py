from nornir import InitNornir


def main():
    nr = InitNornir()
    print()
    for host in nr.inventory.hosts:
        print(f"{host} TZ --> {nr.inventory.hosts[host]['timezone']}")
    print()


if __name__ == "__main__":
    main()
