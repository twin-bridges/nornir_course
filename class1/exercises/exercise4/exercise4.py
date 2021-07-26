from nornir import InitNornir
from random import random
import time


def my_task(task):
    time.sleep(random())
    print()
    print(task.host.hostname)
    print("-" * 12)
    print("These aren't the droids you're looking for.")
    print()


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    nr.run(task=my_task)
