from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")


def my_first_task(task):
    print("Hey, look a task!")


print(type(nr))
print(nr.inventory.hosts)
nr.run(task=my_first_task)
