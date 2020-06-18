import os
from nornir import InitNornir


NBOX_TOKEN = os.environ.get("NETBOX_TOKEN", "sad, no token")


def nbox_task(task):
    print(task.host["site"])
    if task.host["site"] == "area52":
        print("very sneaky switch!")


def main():
    nr = InitNornir(
        config_file="config.yaml",
        inventory={
            "plugin": "NBInventory",
            "options": {
                "nb_token": NBOX_TOKEN,
                "nb_url": "https://netbox.lasthop.io",
                "ssl_verify": False,
            },
        },
    )
    nr.run(task=nbox_task)


if __name__ == "__main__":
    main()
