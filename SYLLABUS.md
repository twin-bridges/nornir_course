# Nornir Online Course


## Week 1
* Overview: Why does Nornir exist? What problem is it trying to solve?
* Nornir System Components: Inventory, Core, Plugins, Tasks, Config
* Inventory System: Internal Object Structure and Schema
* Inventory System: Example using Simple Inventory
* Nornir Plugins and Tasks: Types of Plugins, what is a Task
* Inspect Nornir Inventory using Pdb
* First Nornir Task
* The Behavior of .run()


## Week 2
* Intro to results objects - maybe use networking.tcp_ping task
* Simple netmiko task - get prompt
* Simple napalm task - get facts
* Basic debugging/troubleshooting - how to deal with a failed task; set workers=1, pdb
    * echo data for troubleshooting https://nornir.readthedocs.io/en/stable/plugins/tasks/data.html#nornir.plugins.tasks.data.echo_data


## Week 3
* Inventory system (part2): groups, defaults
* Inventory filtering - get group of junos and group of nxos for example; run different show commands on each group
* Netmiko -- add in ntc-templates
* NAPALM -- expanded use; add in getters

## Week 4
* Subtasks
* Results and dealing w/ subtasks
* can probably add some meat here -- configure bgp, check peers, that type of thing

## Week 5
* Inventory system (part3): add in data to the hosts/groups for building actual configs out
* Jinja2 templating with Nornir
* More advanced Jinja2 -- extends, ???

## Week 6
* config.yaml: nornir config options, core/inventory/logging/etc.?
* transform_function: simple example like this: https://github.com/nornir-automation/nornir/issues/278
* ConnectionOptions - manually manage some connection option -- for example try custom API port, if it fails manually reset connection option to standard API port

## Week 7
* Best Practice: rasie_on_error, num_workers, password security (env vars, vault, etc.)
* dry_run: sometimes useful, why would we want to use it, how do we use it
* Ansible Inventory plugin -- basic example
* future/in progress stuff -- NETCONF plugin, ???


## Other stuff
sftp/write_file
http_method
???





