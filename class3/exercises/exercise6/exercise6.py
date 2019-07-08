from pprint import pprint
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(groups=["nxos"])
    result = nr.run(
        task=napalm_get,
        getters=["config", "facts"],
        getters_options={"config": {"retrieve": "all"}},
    )
    combined_data = {}
    for res in result:
        combined_data[res] = {}
        config_get = result[res][0].result["config"]
        # Remove first four lines of configuration which contain a timestamp
        config_start = config_get["startup"].split("\n")[4:]
        config_running = config_get["running"].split("\n")[4:]
        fact_get = result[res][0].result["facts"]
        if config_running == config_start:
            combined_data[res]["start_running_match"] = True
        else:
            combined_data[res]["start_running_match"] = False
        combined_data[res]["vendor"] = fact_get["vendor"]
        combined_data[res]["model"] = fact_get["model"]
        combined_data[res]["uptime"] = fact_get["uptime"]
    pprint(combined_data)


if __name__ == "__main__":
    main()
