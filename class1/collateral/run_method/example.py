import random
import time
from nornir import InitNornir


def my_task(task):
    time.sleep(random.random())
    print(task.host)


def main():
    nr = InitNornir(core={"num_workers": 1})
    nr.run(task=my_task)


if __name__ == "__main__":
    main()
