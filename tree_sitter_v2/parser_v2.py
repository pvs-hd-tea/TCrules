import os
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

pyparse = parser_py.parse(bytes("name = 1", "utf-8")).root_node.sexp()
jvparse = parser_jv.parse(bytes("name = 1;", "utf-8")).root_node.sexp()
cppparse = parser_cpp.parse(bytes("name = 1;", "utf-8")).root_node.sexp()


# print(pyparse)
# print(pyparse.node.type)
# pyparse.goto_first_child()
# print(pyparse.node.type)
# pyparse.goto_next_sibling()
# print(pyparse.node.type)
# print("----------------------------------------")
print(jvparse)
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


keywords = ["assignment","assignment_expression"]
jvparse = parser_jv.parse(bytes("name = 1;", "utf-8")).root_node.walk()


#input requires parse tree with called attribute walk() 
def check_for_match(input_parse_tree):
    possible = True
    while(possible):
        input_parse_tree.goto_first_child()
        if input_parse_tree.node.type in keywords:
            print("great success")
            possible = False


    

