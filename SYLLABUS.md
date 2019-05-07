# Nornir Online Course


## Week 1
* Overview: Why does Nornir exist? What problem is it trying to solve?
* Nornir System Components: Inventory, Core, Plugins, Tasks, Config
* Inventory System: Internal Object Structure and Schema
* Inventory System: Example using Simple Inventory
* Inspect Nornir Inventory using Pdb
* Nornir Plugins and Tasks: Types of Plugins, what is a Task
* First Nornir Task
* The Behavior of .run()

## Week 2
* Introduction to Results Objects
* Simple Netmiko Task: Show Command
* Inventory System: Groups, Defaults
* Simple NAPALM Task: get_facts
* Basic Nornir Debugging and Troubleshooting

## Week 3
* Inventory System: Order of Preference (hosts, groups, defaults)
* Inventory Filtering
* Netmiko + TextFSM
* NAPALM: Expanded Getters

## Week 4
* Subtasks
* Results and Handling Subtasks
* Netmiko File Copy
* Netmiko Configuration Operations
* NAPALM Configuration Operations

## Week 5
* Inventory System: Data
* Inventory System: ConnectionOptions
* Loading Additional Data
* Jinja2 templating with Nornir
* Jinja2 and Pushing Configurations Using Netmiko/NAPALM Plugins

## Week 6
* config.yaml: Nornir Config Options
* Environment Variables
* Handling Passwords/Keys
* Handling Exceptions and Failed Hosts

## Bonus Lesson
* transform_function: simple example like this: https://github.com/nornir-automation/nornir/issues/278
* dry_run: sometimes useful, why would we want to use it, how do we use it
* Ansible Inventory plugin -- basic example
* future/in progress stuff -- NETCONF plugin, ???


## Other stuff
sftp/write_file
http_method
secret management
transform_function, NETCONF, Ansible Inventory?
http_command and netbox
Nornir logging 
Nornir config file/environment variables.
Generic data loading
echo data for troubleshooting https://nornir.readthedocs.io/en/stable/plugins/tasks/data.html#nornir.plugins.tasks.data.echo_data 
how to deal with a failed task; set workers=1, pdb
Inventory handling when both Netmiko and NAPALM are present in inventory
Setting enable secret dynamically
Raise_on_error behavior
