from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")

for host_name, host_obj in nr.inventory.hosts.items():
    print()
    print(f"Host: {host_name}")
    print("-" * 20)
    print(f"hostname: {host_obj.hostname}")
    print(f"groups: {host_obj.groups}")
    print(f"platform: {host_obj.platform}")
    print(f"username: {host_obj.username}")
    print(f"password: {host_obj.password}")
    print(f"port: {host_obj.port}")
    print()
