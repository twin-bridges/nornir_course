import re

from nornir import InitNornir
from nornir.plugins.tasks import networking

HOUR_SECONDS = 3600
DAY_SECONDS = 24 * HOUR_SECONDS
WEEK_SECONDS = 7 * DAY_SECONDS
YEAR_SECONDS = 365 * DAY_SECONDS


def parse_uptime(uptime_str):
    """Based on method in the NAPALM library"""

    if 'uptime is' in uptime_str:
        uptime_str = uptime_str.split("uptime is")[1]
        uptime_str = uptime_str.strip()

    # Initialize to zero
    (years, weeks, days, hours, minutes) = (0, 0, 0, 0, 0)

    uptime_str = uptime_str.strip()
    time_list = uptime_str.split(",")
    for element in time_list:
        if re.search("year", element):
            years = int(element.split()[0])
        elif re.search("week", element):
            weeks = int(element.split()[0])
        elif re.search("day", element):
            days = int(element.split()[0])
        elif re.search("hour", element):
            hours = int(element.split()[0])
        elif re.search("minute", element):
            minutes = int(element.split()[0])

    uptime_sec = (
        (years * YEAR_SECONDS)
        + (weeks * WEEK_SECONDS)
        + (days * DAY_SECONDS)
        + (hours * 3600)
        + (minutes * 60)
    )
    return uptime_sec


def uptime(task):

    host = task.host
    platform = host.platform

    cmd_mapper = {
        "ios": "show version | inc uptime",
        "eos": "show version | inc Uptime",
        "nxos": "show version | inc uptime",
        "junos": "show system uptime | match System"
    }
    cmd = cmd_mapper[platform]
    multi_result = task.run(task=networking.netmiko_send_command, command_string=cmd)
    uptime_output = multi_result[0].result

    import ipdb; ipdb.set_trace()
    if platform != "junos":
        uptime_sec = parse_uptime(uptime_output)
    else:
        return None

    if uptime_sec >= DAY_SECONDS:
        print()
        print("-" * 40)
        print(f"{host.name}: Up more than a day")
        print(uptime_sec)
        print("-" * 40)
        print()


def main():
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=uptime, num_workers=1)


if __name__ == "__main__":
    main()
