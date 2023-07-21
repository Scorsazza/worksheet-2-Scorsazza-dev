import json
import pathlib
import random

__dirpath__ = pathlib.Path(globals().get("__file__", "./_")).absolute().parent


def generate_random_scores():
    p = pathlib.Path(__dirpath__.__str__() + "/scores.json")
    if not p.is_file():  # or p.is_dir() to see if it is a directory
        names = []
        with open(__dirpath__.__str__() + "/names.txt") as file:
            for line in file:
                names.append(line.strip())

        scores = [[100000, "Tom"], [99999, "James"]]

        for i in range(10):
            scores.append([random.randint(1000, 9999), names[random.randint(0, len(names) - 1)]])

        for i in range(9988):
            scores.append([random.randint(100, 1500), names[random.randint(0, len(names) - 1)]])

        file = open(__dirpath__.__str__() + "/scores.json", "w")
        file.write(json.dumps(scores))
        file.close()
