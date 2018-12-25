from json import load


def ParseSourceCode(json):
    data = load(json)

    key   = data[0]["file"]
    value = data[0]["command"]

    commands = dict()
    commands[key] = value

    return commands

