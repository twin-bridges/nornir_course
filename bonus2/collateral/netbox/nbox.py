import os
from nornir import InitNornir


NBOX_TOKEN = os.environ.get("NETBOX_TOKEN", "sad, no token")


def nbox_task(task):
    if task.host["site"] == "area52":
        print("very sneaky switch!")


def main():
    nr = InitNornir(
        config_file="config.yaml",
        inventory={
            "options": {"nb_token": NBOX_TOKEN, "nb_url": "https://netbox.lasthop.io"}
        },
    )
    nr.run(task=nbox_task)


if __name__ == "__main__":
    main()
