import ipdb
from nornir import InitNornir


def main():
    nr = InitNornir(
        inventory={
            "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
            "options": {"host_file": "inventory.yaml"},
        }
    )
    ipdb.set_trace()


if __name__ == "__main__":
    main()
