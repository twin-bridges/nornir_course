import pdbr  # noqa
from rich import print
from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    print(nr.inventory.hosts)
    print(nr.inventory.groups)
    # pdbr.set_trace()


if __name__ == "__main__":
    main()
