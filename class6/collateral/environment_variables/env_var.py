import os
from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    for host, host_obj in nr.inventory.hosts.items():
        host_obj.password = os.environ.get("NORNIR_PASSWORD", "bogus")
        host_obj.username = os.environ.get("NORNIR_USERNAME", "pyclass")
        print(host_obj.password)
        print(host_obj.username)


if __name__ == "__main__":
    main()
