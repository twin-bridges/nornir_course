import ipdb  # noqa
from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get


def napalm_custom(task):

    # ipdb.set_trace()

    # Dynamically set the session_log to be unique per host
    filename = f"{task.host}-output.txt"
    group_object = task.host.groups[0]
    group_object.connection_options["napalm"].extras["optional_args"][
        "session_log"
    ] = filename

    results = task.run(task=napalm_get, getters=["facts"])
    print(results)


if __name__ == "__main__":
    nr = InitNornir(config_file="config_serial.yaml")
    nr = nr.filter(F(groups__contains="ios"))
    results = nr.run(task=napalm_custom)

    print()
    for k, v in results.items():
        print("-" * 50)
        print(k)
        print(v[1].result)
        print("-" * 50)
    print()
