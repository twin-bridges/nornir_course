from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    nxos1 = nr.inventory.hosts["nxos1"]

    print()
    print(nr.inventory.hosts)
    print(f"Username: {nxos1.username}")
    print(f"Password: {nxos1.password}")
    print(f"Port: {nxos1.port}")
    print(f"Platform: {nxos1.platform}")
    print(f"NAPALM Port: {nxos1.get_connection_parameters('napalm').port}")
    print()


if __name__ == "__main__":
    main()
