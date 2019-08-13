from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista4")

    # Capture current running configuration
    result = nr.run(task=networking.napalm_get, getters=["config"], retrieve="running")
    print_result(result)
    arista4_running_config = result["arista4"][0].result["config"]["running"]

    # Configure a new loopback
    config = """interface loopback123
  description verycoolloopback"""
    result = nr.run(task=networking.napalm_configure, configuration=config)
    print_result(result)

    input = ("Pause here to verify the state")

    # Completely resture the configuration using configure replace
    result = nr.run(
        task=networking.napalm_configure,
        configuration=arista4_running_config,
        replace=True,
    )
    print_result(result)


if __name__ == "__main__":
    main()
