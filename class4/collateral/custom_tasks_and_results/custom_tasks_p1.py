from nornir import InitNornir


def my_task(task):
    import ipdb; ipdb.set_trace()
    print("Hello, World!")


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr.run(task=my_task, num_workers=1)


if __name__ == "__main__":
    main()
