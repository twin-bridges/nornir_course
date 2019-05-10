# Nornir Online Course


## Week 1
* Overview: Why does Nornir exist? What problem is it trying to solve?
* Nornir System Components: Inventory, Config, Core Execution, Tasks, Results
* Nornir's Inventory System
* Inventory Example
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
* Nornir Logging
* Troubleshooting/Debugging

## Bonus Lesson
* transform_function
* dry_run
* Ansible Inventory Plugin
* sftp
* write_file
* http_method
* NETCONF
* http_command and NetBox
* Inventory handling when both Netmiko and NAPALM are present in inventory
* Setting enable secret dynamically

.
├── apis
│   ├── http_method.py
├── commands
│   ├── command.py
│   └── remote_command.py
├── data
│   ├── echo_data.py
│   ├── load_json.py
│   └── load_yaml.py
├── files
│   ├── sftp.py
│   └── write_file.py
├── __init__.py
├── networking
│   ├── napalm_cli.py
│   ├── napalm_configure.py
│   ├── napalm_get.py
│   ├── napalm_validate.py
│   ├── netmiko_file_transfer.py
│   ├── netmiko_save_config.py
│   ├── netmiko_send_command.py
│   ├── netmiko_send_config.py
│   └── tcp_ping.py
├── text
│   ├── template_file.py
│   └── template_string.py
└── version_control
    ├── gitlab.py
