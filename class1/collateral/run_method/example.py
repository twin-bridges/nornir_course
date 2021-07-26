import random
import time
from nornir import InitNornir


def my_task(task):
    time.sleep(random.random())
    print(task.host)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr.run(task=my_task)


if __name__ == "__main__":
    main()
