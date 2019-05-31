from nornir import InitNornir


def my_task(task):
    print("\nThese aren't the droids you're looking for.\n")


if __name__ == "__main__":
    nr = InitNornir(config_file="nornir.yaml")
    nr.run(task=my_task)
