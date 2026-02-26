import json


def save_report(results, path):
    results.sort(key=lambda x: x["score"], reverse=True)

    with open(path, "w") as f:
        json.dump(results, f, indent=4)