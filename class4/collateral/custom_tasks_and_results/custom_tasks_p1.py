from nornir import InitNornir


def my_task(task):
    # import pdbr
    # pdbr.set_trace()
    print("Hello, World!")


def main():
    nr = InitNornir(
        config_file="config.yaml",
        logging={"enabled": False},
        runner={"plugin": "serial", "options": {}},
    )
    nr.run(task=my_task)


if __name__ == "__main__":
    main()
