from nornir import InitNornir


def main():
    nr = InitNornir(
        config_file="config.yaml",
        runner={"plugin": "threaded", "options": {"num_workers": 15}},
    )
    workers = nr.config.runner.options
    print(f"\nNumber of workers: {workers['num_workers']}\n")


if __name__ == "__main__":
    main()
