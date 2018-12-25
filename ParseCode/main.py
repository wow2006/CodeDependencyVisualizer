import json
import clang.cindex

from DotGenerator import *
from ParseSourceCode import *


def splitCommand(command):
    args = command.split()

    includes_list = [x for x in args if "-I" in x]

    indecies = [(i, i+1) for i,x in enumerate(args) if "-isystem" in x]

    for x, y in indecies:
        includes_list.append(args[x] + " " + args[y])

    return includes_list

def processClassField(cursor):
    """ Returns the name and the type of the given class field.
    The cursor must be of kind CursorKind.FIELD_DECL"""
    type = None
    fieldChilds = list(cursor.get_children())

    if len(fieldChilds) == 0:
        # if there are not cursorchildren, the type is some primitive datatype
        type = cursor.type.spelling
    else:
        # if there are cursorchildren, the type is some non-primitive datatype (a class or class template)
        for cc in fieldChilds:
            if cc.kind == clang.cindex.CursorKind.TEMPLATE_REF:
                type = cc.spelling
            elif cc.kind == clang.cindex.CursorKind.TYPE_REF:
                type = cursor.type.spelling

    name = cursor.spelling
    return name, type

def processClassMemberDeclaration(umlClass, cursor):
    """
    Processes a cursor corresponding to a class member
    declaration and appends the extracted information
    to the given umlClass
    """
    if cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
        for baseClass in cursor.get_children():
            if baseClass.kind == clang.cindex.CursorKind.TEMPLATE_REF:
                umlClass.parents.append(baseClass.spelling)
            elif baseClass.kind == clang.cindex.CursorKind.TYPE_REF:
                umlClass.parents.append(baseClass.type.spelling)
    elif cursor.kind == clang.cindex.CursorKind.FIELD_DECL:  # non static data member
        name, type = processClassField(cursor)
        if name is not None and type is not None:
            # clang < 3.5: needs patched cindex.py to have
            # clang.cindex.AccessSpecifier available:
            # https://gitorious.org/clang-mirror/clang-mirror/commit/e3d4e7c9a45ed9ad4645e4dc9f4d3b4109389cb7
            if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
                umlClass.publicFields.append((name, type))
            elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
                umlClass.privateFields.append((name, type))
            elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
                umlClass.protectedFields.append((name, type))
    elif cursor.kind == clang.cindex.CursorKind.CXX_METHOD:
        try:
            returnType, argumentTypes = cursor.type.spelling.split(' ', 1)
            if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
                umlClass.publicMethods.append((returnType, cursor.spelling,
                                               argumentTypes))
            elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
                umlClass.privateMethods.append((returnType, cursor.spelling,
                                                argumentTypes))
            elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
                umlClass.protectedMethods.append((returnType, cursor.spelling,
                                                  argumentTypes))
        except:
            logging.error("Invalid CXX_METHOD declaration! " +
                          str(cursor.type.spelling))
    elif cursor.kind == clang.cindex.CursorKind.FUNCTION_TEMPLATE:
        returnType, argumentTypes = cursor.type.spelling.split(' ', 1)
        if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
            umlClass.publicMethods.append((returnType, cursor.spelling,
                                           argumentTypes))
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
            umlClass.privateMethods.append((returnType, cursor.spelling,
                                            argumentTypes))
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
            umlClass.protectedMethods.append((returnType, cursor.spelling,
                                              argumentTypes))

def processClass(cursor, inclusionConfig):
    """ Processes an ast node that is a class. """
    umlClass = UmlClass()

    # umlClass is the datastructure for the DotGenerator
    # that stores the necessary information about a single class.
    # We extract this information from the clang ast hereafter ...
    if cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE:
        # process declarations like:
        #   template <typename T> class MyClass
        umlClass.fqn = cursor.spelling
    else:
        # process declarations like:
        #   class MyClass ...
        #   struct MyStruct ...
        umlClass.fqn = cursor.type.spelling  # the fully qualified name

    import re
    if (inclusionConfig['excludeClasses'] and
        re.match(inclusionConfig['excludeClasses'], umlClass.fqn)):
        return

    if (inclusionConfig['includeClasses'] and not
        re.match(inclusionConfig['includeClasses'], umlClass.fqn)):
        return

    for c in cursor.get_children():
        # process member variables and methods declarations
        processClassMemberDeclaration(umlClass, c)

    print(umlClass)

def traverseAst(cursor, inclusionConfig):
    if (cursor.kind == clang.cindex.CursorKind.CLASS_DECL or
        cursor.kind == clang.cindex.CursorKind.STRUCT_DECL or
        cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE):
        # if the current cursor is a class, class template or struct declaration,
        # we process it further ...
        processClass(cursor, inclusionConfig)

    for child_node in cursor.get_children():
        traverseAst(child_node, inclusionConfig)

def parseTranslationUnit(filePath, includeDirs, inclusionConfig):
    index = clang.cindex.Index.create()

    clangArgs = ['-x', 'c++', *includeDirs]

    tu = index.parse(filePath, args=clangArgs,
        options=clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)

    traverseAst(tu.cursor, inclusionConfig)

if __name__ == "__main__":
    json_name = "compile_commands.json"

    with open(json_name, "r") as json_file:
        json_data = ParseSourceCode(json_file)

    for file_name in json_data:
        parseTranslationUnit(file_name,
                             json_data[file_name],
                             "")

