from json import load


def ParseSourceCode(json):
    data = load(json)
    commands = dict()

    for item in data:
        key   = item["file"]
        value = item["command"]

        commands[key] = value

    return commands

