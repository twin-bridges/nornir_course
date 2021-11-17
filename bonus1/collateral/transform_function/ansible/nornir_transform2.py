"""
export NORNIR_INVENTORY_TRANSFORM_FUNCTION=transform_func
"""
from nornir import InitNornir
from nornir.core.plugins.inventory import TransformFunctionRegister


def transform_ansible(host):
    if "nxos" == host.groups[0].name:
        napalm_params = host.get_connection_parameters("napalm")
        napalm_params.port = 8443
        host.connection_options["napalm"] = napalm_params


def main():
    nr = InitNornir(config_file="config_transform.yaml")
    napalm_params = nr.inventory.hosts["nxos1"].get_connection_parameters("napalm")

    napalm_params = nr.inventory.hosts["nxos1"].get_connection_parameters("napalm")
    print(napalm_params.dict())


if __name__ == "__main__":
    TransformFunctionRegister.register("transform_func", transform_ansible)
    main()
