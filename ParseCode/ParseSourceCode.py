from json import load
import clang.cindex


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

        commands[key] = ParseCommand(value)

    return commands

def CreateAST(file_info):
    index = clang.cindex.Index.create()
    for key in file_info:
        tu = index.parse(key, args=file_info[key],
                         options=clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)
    
    if not tu:
        raise Exception("ExpectedException not raised")

    return tu

def TraverseAST(TransUnit):
    pass

