import os
from tabnanny import check
from tree_sitter import Language, Parser
from fuzzywuzzy import fuzz
import re
import json

PYTHON = "PYTHON"
JAVA = "JAVA"
CPP = "CPP"

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    # Jonas
    [
        '/Users/jonas/Documents/GitHub/tree-sitter-cpp',
        '/Users/jonas/Documents/GitHub/tree-sitter-java',
        '/Users/jonas/Documents/GitHub/tree-sitter-python'
    ]
    # Vivian
    # [
    #     '/home/vivi/src/tree-sitter-python',
    #     '/home/vivi/src/tree-sitter-java',
    #     '/home/vivi/src/tree-sitter-cpp'
    # ]
)

PY_LANGUAGE = Language('build/my-languages.so', 'python')
JV_LANGUAGE = Language('build/my-languages.so', 'java')
CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')



"""Create Parser"""
parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)

parser_jv = Parser()
parser_jv.set_language(JV_LANGUAGE)

parser_cpp = Parser()
parser_cpp.set_language(CPP_LANGUAGE)

pyparse = parser_py.parse(bytes("name = 1", "utf-8")).root_node.walk()
jvparse = parser_jv.parse(bytes("name = 1;", "utf-8")).root_node.walk()
cppparse = parser_cpp.parse(bytes("name = 1;", "utf-8")).root_node.walk()


# print(pyparse)
# print(pyparse.node.type)
# pyparse.goto_first_child()
# print(pyparse.node.type)
# pyparse.goto_next_sibling()
# print(pyparse.node.type)
# print("----------------------------------------")
# print(jvparse)
# jvparse.goto_first_child()
# print(jvparse.node.type)
# jvparse.goto_next_sibling()
# print(jvparse.node.type)
# print("----------------------------------------")
# print(cppparse)
# cppparse.goto_first_child()
# print(cppparse.node.type)
# cppparse.goto_next_sibling()
# print(jvparse.node.type)


keywords = ["assignment","assignment_expression","declaration","local_variable_declaration"]



def create_parse_tree(input_code, input_language):
    '''creates a parse tree for given input code and input language'''
    if input_language == "PYTHON":
        return parser_py.parse(bytes(input_code, "utf-8")).root_node.sexp()
    elif input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8")).root_node.sexp()
    elif input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8")).root_node.sexp()


def check_for_match(input_parse_tree):
    for keyword in keywords:
        if keyword in input_parse_tree:
            return keyword


if __name__ == "__main__":
    print("Input code:")
    input_code = input()
    print("Input language:")
    input_language = input()
    tree = create_parse_tree(input_code, input_language)
    type = check_for_match(tree)
    num = re.findall(r'\d+', input_code)
    print(type + "(" + num[0] + ")")

