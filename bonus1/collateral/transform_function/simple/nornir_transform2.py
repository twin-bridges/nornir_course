"""
export NORNIR_INVENTORY_TRANSFORM_FUNCTION=transform_func
"""
import os
from nornir import InitNornir
from nornir.core.plugins.inventory import TransformFunctionRegister


def transform_automation_user(host):
    host.username = "automaton"
    host.password = os.environ.get("AUTOMATION_USER_PASSWORD", "bogus")


def main():
    nr = InitNornir(config_file="config_transform.yaml")
    print(f"{nr.inventory.hosts['srx2'].username}")


if __name__ == "__main__":
    TransformFunctionRegister.register("transform_func", transform_automation_user)
    main()
