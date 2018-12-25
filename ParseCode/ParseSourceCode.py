from json import load


def ParseSourceCode(json):
    with open(json, "r") as json_file:
        data = load(json_file)

    key   = data[0]["file"]
    value = data[0]["command"]

    commands = dict()
    commands[key] = value

    return commands

