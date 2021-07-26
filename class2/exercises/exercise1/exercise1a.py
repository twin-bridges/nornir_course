from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config1a.yaml")
    # Print default of 20 workers (new format Nornir >= 3.0.0)
    workers = nr.config.runner.options
    workers = 20 if workers == {} else workers["num_workers"]
    print(f"\nNumber of workers: {workers}\n")


if __name__ == "__main__":
    main()
