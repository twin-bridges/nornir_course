## Nornir Version3 Incompatible Changes

### Plugins are no included with Nornir Core

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
