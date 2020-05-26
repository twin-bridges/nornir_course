from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    # New Nornir 3.x format
    workers = nr.config.runner.options
    print(f"\nNumber of workers: {workers['num_workers']}\n")


if __name__ == "__main__":
    main()
