import ipdb  # noqa
from nornir import InitNornir


def example_task(task):
    return f"This is a nornir task executed against {task.host}"


def main():
    nr = InitNornir()
    aggresult = nr.run(task=example_task)
    mulresult = aggresult["localhost2"]
    result = mulresult[0]
    print(result)
    # ipdb.set_trace()


if __name__ == "__main__":
    main()
