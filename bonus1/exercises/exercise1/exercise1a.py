from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    print(nr.inventory.hosts)
    nxos1 = nr.inventory.hosts["nxos1"]
    print(nxos1.username)
    print(nxos1.password)
    print(nxos1.port)
    print(nxos1.platform)
    print(nxos1.get_connection_parameters("napalm").port)


if __name__ == "__main__":
    main()
