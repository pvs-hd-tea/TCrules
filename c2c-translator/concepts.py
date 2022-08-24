import os
import json
from tree_sitter import Language, Parser
from fuzzywuzzy import fuzz

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    [
        '/Users/jonas/Documents/GitHub/tree-sitter-cpp',
        '/Users/jonas/Documents/GitHub/tree-sitter-java',
        '/Users/jonas/Documents/GitHub/tree-sitter-python'
    ]
)

PY_LANGUAGE = Language('build/my-languages.so', 'python')
JV_LANGUAGE = Language('build/my-languages.so', 'java')
CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

CPP = "CPP"
PYTHON = "PYTHON"
JAVA = "JAVA"

# Create Parsers for the three languages
parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)

parser_jv = Parser()
parser_jv.set_language(JV_LANGUAGE)

parser_cpp = Parser()
parser_cpp.set_language(CPP_LANGUAGE)


class Concept:
    """class for the database maintaining concepts"""

    def __init__(self):
        if not os.path.isfile("concepts.json"):
            self.concepts = {}
        else:
            with open("concepts.json", encoding="utf8") as file:
                self.concepts = json.load(file)
                print(f"Loading {len(self.concepts)} concepts ... Done ...")

    def save_concepts(self):
        """store derived rules in json format"""
        with open("concepts.json", "a+", encoding="utf8") as file:
            file.truncate(0)
            file.seek(0)
            json.dump(self.concepts, file, indent=4)


    def extend_concept(self, cpp, java, python, key):
        """extend existing concept '<key>' by list of generic expressions, one for each language"""
        generic_cpp = self.create_generic_expression(cpp)
        generic_jv = self.create_generic_expression(java, JAVA.lower())
        generic_py = self.create_generic_expression(python, PYTHON.lower())

        if generic_cpp and len(generic_cpp) - len(generic_cpp.lstrip()) == 0 and generic_jv and generic_py:
            flag = False

            for entry in self.concepts[key]:
                if generic_cpp in entry:
                    flag = True
                    break  # already present

            if not flag:
                self.concepts[key].append([generic_cpp, generic_jv, generic_py])

    def add_concept(self, cpp, java, python, key):
        """add new concept to the database"""
        generic_cpp = self.create_generic_expression(cpp)
        generic_jv = self.create_generic_expression(java, JAVA.lower())
        generic_py = self.create_generic_expression(python, PYTHON.lower())

        if generic_cpp and generic_jv and generic_py:
            self.concepts.update({key: [[generic_cpp, generic_jv, generic_py]]})

    def user_input(self, keyword=None):
        """Check for well known concept"""
        print("Please enter the name of the concept below. Try not to enter a concept twice and check for existing names first")
        print("Does one of the entries describe your code's concept?")
        with open ("concepts.json") as concepts:
            keys = list(concepts.keys())
        print(keys)
        print("If it doesn't resemble any concept, please enter a new one. Please try to consider newlines and indents for better accuracy in translations")
        cpp = input("CPP: ")
        java = input("JAVA: ")
        python = input("PYTHON: ")

        if keyword in self.concepts.keys():
            self.extend_concept(cpp, java, python, keyword)
        else:
            self.add_concept(cpp, java, python, keyword)

    def check_similarity(self,input_code, input_language):
        parse_tree = create_parse_tree(input_code,input_language)
        with open("concepts.json") as concepts:
            values = list(concepts.values())
        java_trees = []
        cpp_trees = []
        python_trees = []

        if input_language == JAVA:
            for value in values:
                tree = parser_jv.parse(bytes(value, "utf-8")).root_node.sexp()
                ratio = fuzz.partial_ratio(parse_tree,tree)
        if input_language == CPP:
            for value in values:
                tree = parser_jv.parse(bytes(value, "utf-8")).root_node.sexp()
                ratio = fuzz.partial_ratio(parse_tree,tree)
        if input_language == PYTHON:
            for value in values:
                tree = parser_jv.parse(bytes(value, "utf-8")).root_node.sexp()
                ratio = fuzz.partial_ratio(parse_tree,tree)
        
            


def create_parse_tree(input_code, input_language):
    """return s-expression and parse tree for the given code and language using the tree-sitter"""
    if input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8")).root_node.sexp(), parser_cpp.parse(bytes(input_code, "utf-8"))
    if input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8")).root_node.sexp(), parser_jv.parse(bytes(input_code, "utf-8"))
    return parser_py.parse(bytes(input_code, "utf-8")).root_node.sexp(), parser_py.parse(bytes(input_code, "utf-8"))





concept = Concept()
concept.save_concepts()



input_code = "list_ = [1,3,4,2]\n list_.sort()"
tree_one = parser_py.parse(bytes(input_code, "utf-8")).root_node.sexp()

input_code_two = "list_ = [1,3,4,2,2,7,5]\n list_.sort()"
tree_two = parser_py.parse(bytes(input_code_two, "utf-8")).root_node.sexp()

input_code_three = "list_ = [1,3,4,2,2,7,5]\n list_f = [1,3,4,2,2,7,5]\nlist_ g= [1,3,4,2,2,7,5]\nlist_.sort()"
tree_three = parser_py.parse(bytes(input_code_three, "utf-8")).root_node.sexp()

print(fuzz.partial_ratio(tree_one, tree_two))
print(fuzz.partial_ratio(tree_one, tree_three))