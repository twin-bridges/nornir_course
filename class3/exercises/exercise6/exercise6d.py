from pprint import pprint
from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get


def main():

    # Exercise 6a
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))

    agg_result = nr.run(
        task=napalm_get,
        getters=["config", "facts"],
        getters_options={"config": {"retrieve": "all"}},
    )

    combined_data = {}
    for device_name, multi_result in agg_result.items():

        combined_data[device_name] = {}
        device_result = multi_result[0]

        # Retrieve the NAPALM "configuration" getter info
        config_get = device_result.result["config"]

        # Remove first four lines of configuration which contain a timestamp
        config_start = config_get["startup"].split("\n")[4:]
        config_running = config_get["running"].split("\n")[4:]

        # Retrieve the NAPALM "facts"
        fact_get = device_result.result["facts"]

        # Update combined_data for this device
        if config_running == config_start:
            combined_data[device_name]["start_running_match"] = True
        else:
            combined_data[device_name]["start_running_match"] = False
        combined_data[device_name]["vendor"] = fact_get["vendor"]
        combined_data[device_name]["model"] = fact_get["model"]
        combined_data[device_name]["uptime"] = fact_get["uptime"]

    pprint(combined_data)


if __name__ == "__main__":
    main()
