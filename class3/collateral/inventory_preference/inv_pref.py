from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    print(nr.inventory.hosts)
    print(nr.inventory.groups)
    # import ipdb
    # ipdb.set_trace()


if __name__ == "__main__":
    main()
