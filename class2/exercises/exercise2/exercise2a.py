import os
from nornir import InitNornir
from nornir.core.filter import F


def main():
    nr = InitNornir(config_file="config.yaml")
    # Avoid storing lab password in GitHub, pull from environment variable
    nr.inventory.defaults.password = os.environ["NORNIR_PASSWORD"]
    filt = F(groups__contains="ios")
    nr = nr.filter(filt)
    print(nr.inventory.hosts)


if __name__ == "__main__":
    main()
