from json import load


def ParseCommand(command):
    args = command.split()

    includes_list = [x for x in args if "-I" in x]

    return includes_list

def ParseSourceCode(json):
    data = load(json)
    commands = dict()

    for item in data:
        key   = item["file"]
        value = item["command"]

        commands[key] = value

    return commands

