## Nornir Version3 Incompatible Changes

### Plugins are not included with Nornir Core

Most plugins are no longer included with Nornir Core. Consequently, you will need to separately PIP install these plugins and then update the imports in your code.

For a list of common Nornir Plugins see:

https://nornir.tech/nornir/plugins/

Here are some example code changes pertaining to this change:

```diff
- from nornir.plugins.functions.text import print_result
- from nornir.plugins.tasks.networking import netmiko_send_command
+ from nornir_utils.plugins.functions import print_result
+ from nornir_netmiko import netmiko_send_command
```

```diff
- from nornir.plugins.tasks.networking import napalm_get
+ from nornir_napalm.plugins.tasks import napalm_get
```

```diff
- from nornir.plugins.tasks.text import template_file
- from nornir.plugins.tasks.files import write_file
+ from nornir_jinja2.plugins.tasks import template_file
+ from nornir_utils.plugins.tasks.files import write_file
```

### Inventory Plugin Names Simplified

Inventory plugins are also plugins and consequently no longer distributed with Nornir Core. Consequently, you will generally need to PIP install Nornir inventory plugins (with the exception of SimpleInventory which is distributed with Nornir Core).

Entry points are also now used for inventory plugins which simplifies their naming (see below):

```diff
# Example Nornir config.yaml
inventory:
-  plugin: nornir.plugins.inventory.simple.SimpleInventory
+  plugin: SimpleInventory
  options:
    host_file: "hosts.yaml"
    group_file: "groups.yaml"
    defaults_file: "defaults.yaml"
```

Or in the case of in-line Python code using the NetBox Inventory plugin:

```diff
def main():
    nr = InitNornir(
        config_file="config.yaml",
        inventory={
-            "plugin": "nornir.plugins.inventory.netbox.NBInventory",
+            "plugin": "NBInventory",
            "options": {
                "nb_token": NBOX_TOKEN,
                "nb_url": "https://netbox.domain.com",
                "ssl_verify": False,
            },
        },
    )
    nr.run(task=nbox_task)
```

Note, the above is using the legacy NetBox inventory plugin (NBInventory). There is a newer NetBox inventory plugin (NetBoxInventory2). See https://github.com/wvandeun/nornir_netbox for more details on NetBoxInventory2.

### Runners and num_workers changes

You can no longer specify `num_workers` as an argument directly to nr.run. The easiest mechanism of controlling the number of works is now through your Nornir config.yaml settings.

This is done in the new `runners` section of config.yaml. For example,

```yaml
runner:
  plugin: threaded
  options:
    num_workers: 10
```

Similarly, you can no longer toggle between serial execution and threaded execution by setting num_workers=1 instead you need to change the `runner` to be `plugin: serial`.

For example:

```yaml
runner:
  plugin: serial
```

The runner and associated arguments can also be specified using in-line Python code:

```python
nr = InitNornir(
    config_file="config.yaml",
    logging={"enabled": False},
    runner={"plugin": "threaded", "options": {"num_workers": 15}},
) 
```
