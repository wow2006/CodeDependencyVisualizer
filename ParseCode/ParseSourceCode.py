from json import load


def ParseCommand(command):
    args = command.split()

    includes_list = [x for x in args if "-I" in x]

    indecies = [(i, i+1) for i,x in enumerate(args) if "-isystem" in x]

    for x, y in indecies:
        includes_list.append(args[x] + " " + args[y])

    return includes_list

def ParseSourceCode(json):
    data = load(json)
    commands = dict()

    for item in data:
        key   = item["file"]
        value = item["command"]

        commands[key] = value

    return commands

