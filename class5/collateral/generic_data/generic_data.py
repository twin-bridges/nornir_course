from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr = nr.filter(name="cisco3")
    cisco3 = nr.inventory.hosts["cisco3"]
    print(cisco3)
    import ipdb

    ipdb.set_trace()


if __name__ == "__main__":
    main()
