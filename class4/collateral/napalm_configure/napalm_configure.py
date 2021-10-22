from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_napalm.plugins.tasks import napalm_configure


arista1_loopback = """interface loopback123
  ip address 1.2.3.4/32
  no shutdown
  description nornir was here!"""

arista2_loopback = """interface loopback123
  ip address 1.2.3.5/32
  no shutdown
  description and here too!"""

test_loopback = "this isnt a loopback!"


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    arista1 = nr.filter(name="arista1")
    arista2 = nr.filter(name="arista2")

    # import pdbr
    # pdbr.set_trace()

    result = arista1.run(task=napalm_configure, configuration=arista1_loopback)
    print_result(result)

    result = arista2.run(task=napalm_configure, filename="arista2_loopback")
    print_result(result)

    # Commenting out the "failure" test
    # result = arista1.run(task=napalm_configure, configuration=test_loopback)
    # print_result(result)

    result = arista2.run(
        task=napalm_configure, configuration=arista2_loopback, dry_run=False
    )
    print_result(result)

    result = arista1.run(task=napalm_get, getters=["config"], retrieve="running")
    arista1_running = result["arista1"].result["config"]["running"]

    arista1.run(task=napalm_configure, configuration="no interface loopback123")

    result = arista1.run(
        task=napalm_configure, configuration=arista1_running, replace=True
    )
    print_result(result)


if __name__ == "__main__":
    main()
