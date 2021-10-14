import pdbr  # noqa
from nornir import InitNornir


def main():
    nr = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {"host_file": "inventory.yaml"},
        }
    )
    print(nr)
    print(nr.inventory.hosts)
    # pdbr.set_trace()


if __name__ == "__main__":
    main()
