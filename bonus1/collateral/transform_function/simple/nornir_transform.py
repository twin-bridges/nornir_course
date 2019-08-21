import os
from nornir import InitNornir


def transform_automation_user(host):
    host.username = "automaton"
    host.password = os.environ.get("AUTOMATION_USER_PASSWORD", "bogus")


def main():
    nr = InitNornir(config_file="config.yaml")
    print(f"{nr.inventory.hosts['srx2'].username}")


if __name__ == "__main__":
    main()
