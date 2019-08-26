from nornir import InitNornir


def transform_ansible(host):
    if "nxos" in host.groups:
        napalm_params = host.get_connection_parameters("napalm")
        napalm_params.port = 8443
        host.connection_options["napalm"] = napalm_params


def main():
    nr = InitNornir(config_file="config.yaml")
    napalm_params = nr.inventory.hosts["nxos1"].get_connection_parameters("napalm")
    print(napalm_params.dict())


if __name__ == "__main__":
    main()
