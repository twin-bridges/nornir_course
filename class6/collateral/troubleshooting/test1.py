from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.core.exceptions import NornirSubTaskError


def int_task(task):
    raise IndexError()

def uptime(task):
    import ipdb; ipdb.set_trace()
    try:
        task.run(task=int_task)
    except NornirSubTaskError:
        print("Caught")
    print("hello")
    raise ValueError()


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="cisco3")
    agg_result = nr.run(task=uptime, num_workers=1)
    import ipdb; ipdb.set_trace()
    for hostname, multi_result in agg_result.items():
        print()
        print("-" * 40)
        print(f"{hostname}: {multi_result[1].result}")
        print("-" * 40)
        print()


if __name__ == "__main__":
    main()
