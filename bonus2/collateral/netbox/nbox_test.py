import os
import pdbr

from nornir import InitNornir
from nornir.core.filter import F


NBOX_TOKEN = os.environ.get("NETBOX_TOKEN", "sad, no token")


def nbox_task(task):
    print(task.host["site"]["name"])


def main():
    nr = InitNornir(
        config_file="config.yaml",
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_token": NBOX_TOKEN,
                "nb_url": "https://netbox.lasthop.io",
                "ssl_verify": False,
                # "filter_parameters": {"site": "aws-us-west1"},
                # "filter_parameters": {"site": "fremont-dc"},
                # "use_platform_slug": True,
                #
                # Newer Netbox (roughly NetBox 3.5) doesn't support this directly
                # "use_platform_napalm_driver": True,
            },
        },
    )
    pdbr.set_trace()

    cisco1 = nr.inventory.hosts["cisco1"]

    # Filter after loaded
    fremont = nr.filter(F(groups__contains="site__fremont-dc"))
    cisco = nr.filter(F(groups__contains="manufacturer__cisco"))

    nr.run(task=nbox_task)


if __name__ == "__main__":
    main()
