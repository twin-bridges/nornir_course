## Nornir Version3 Incompatible Changes

See also:

https://nornir.readthedocs.io/en/3.0.0/upgrading/2_to_3.html

The referenced page includes some additional changes that are not covered here.


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

Inventory plugins are also plugins and consequently no longer distributed with Nornir Core. You will need to PIP install the Nornir inventory plugins (with the exception of SimpleInventory which is distributed with Nornir Core).

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

Similarly, the `NORNIR_CORE_NUM_WORKERS` has been removed and replaced by the `NORNIR_RUNNER_PLUGIN` and the `NORNIR_RUNNER_OPTIONS` environment variables.

### Nornir Configuration Precedence Changed

In Nornir Version3, the configuration precedence (from highest precedence to lowest precedence) is:

```
Inline Python > Configuration File > Environment Vars
```

### Logging Setting is now 'log_file"

Example, Nornir config.yaml change:

```diff
logging:
-  file: ""
+  log_file: nornir.out
```

Certain things did not like the use of the use of the generic term `file`. Consequently, this was updated to be `log_file` instead.

### Group Filtering and Group .refs

Nornir version 2.x had a been of an obscure aspect where there was a difference between accessing the group name as a string versus accessing the Nornir group. For example (this is from `Nornir 2.5.0`):

```
# This code returns the groups the given hosts belong to as a string
ipdb> p task.host.groups                                                                     
['nxos']
ipdb> p task.host.groups[0]                                                                  
'nxos'
```

If you wanted to actually access the Nornir Group object, you would have done accessed the `refs` attribute (once again in Nornir 2.x):

```
# Retrieve the Nornir Group object itself using .refs
ipdb> p task.host.groups.refs                                                                
[Group: nxos]
ipdb> p task.host.groups.refs[0]                                                             
Group: nxos
```

This `refs` behavior has been simplified such that accessing task.host.groups now returns the Nornir Group object and not a string (and the `.refs` attribute no longer exists).

Example from Nornir 3.0.0

```
ipdb> p task.host.groups                                                                     
[Group: nxos]
ipdb> p task.host.groups[0]                                                                  
Group: nxos
```

The `main implication` of this for Nornir end-users `is that certain group-filter patterns no longer work`.

For example, in Nornir 2.X, you used to be able to do group filtering the following way:

```python
# Nornir 2.X example
nr = nr.filter(groups=["nxos"])
```

Notice, here you are saying the groups this host belongs to exactly matches the list that contains the string "nxos". This pattern no longer works. I recommend you switch to the F-filter pattern instead.

```python
# Nornir 3.x example
nr = nr.filter(F(groups__contains="nxos"))
```

Note, there is a minor difference between the two examples. The first example states belongs to this group and only this group whereas the second example just states belongs to this group.

### Transform Function is now an entry point

I found the new Nornir 3.x transform function behavior overly difficult to use. Consequently, I just converted my code to a simpler pattern that largely recreated the Nornir 2.x behavior.

My new Nornir 3.x pattern will be similar to the following:

```python
nr = InitNornir(config_file="config.yaml")

# Recreate Nornir 2.x transform function behavior
for host in nr.inventory.hosts.values():
    transform_func(host)
```

Where `transform_func` is a function that modifies the Nornir host objects. For example:

```python
def transform_func(host):
    password = os.environ["NORNIR_PASSWORD"]
    host.password = password
```

This also implies that I will cease using `transform_function` in the Nornir `config.yaml` file.


