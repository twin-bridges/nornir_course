from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    # Use setting in the config_file: 5 workers
    print(f"\nNumber of workers: {nr.config.core.num_workers}\n")


if __name__ == "__main__":
    main()
