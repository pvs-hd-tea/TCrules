import os
import json
from tree_sitter import Language, Parser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    # Jonas
    #[
    #    '/Users/jonas/Documents/GitHub/tree-sitter-cpp',
    #    '/Users/jonas/Documents/GitHub/tree-sitter-java',
    #    '/Users/jonas/Documents/GitHub/tree-sitter-python'
    #]
    # Vivian
    [
        '/home/vivi/src/tree-sitter-python',
        '/home/vivi/src/tree-sitter-java',
        '/home/vivi/src/tree-sitter-cpp'
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

        if not os.path.isfile("keywords_concept.txt"):
            self.tree_concepts = []
        else:
            with open("keywords_concept.txt", encoding="utf8") as file:
                self.tree_concepts = file.read().split(",")
                print(f"Loading {len(self.tree_concepts)} keywords for concepts ... Done ...")


    def save_concepts(self):
        """store derived rules in json format"""
        with open("concepts.json", "a+", encoding="utf8") as file:
            file.truncate(0)
            file.seek(0)
            json.dump(self.concepts, file, indent=4)


    def save_keywords(self):
        """store keywords from own json"""
        with open("keywords_concept.txt", "a+", encoding="utf8") as file:
            file.truncate(0)
            file.seek(0)
            length = len(self.tree_concepts) - 1
            for i, keyword in enumerate(self.tree_concepts):
                if i == length:
                    file.write(keyword)
                else:
                    file.write(keyword + ",")


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
        with open("concepts.json") as concepts:
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


    def check_similarity(self, input_code, input_language):
        parse_tree = create_parse_tree(input_code, input_language)
    
        if input_language == PYTHON:
            lang_id = "py"
        elif input_language == JAVA:
            lang_id = "jv"
        elif input_language == CPP:
            lang_id = "cpp"
        else:
            return

        lang_matches = []
        for concept in self.tree_concepts:
            if lang_id in concept:
                if input_language == JAVA:
                    tree = parser_jv.parse(bytes(self.concepts[concept][0][0], "utf-8")).root_node.sexp()
                elif input_language == CPP:
                    tree = parser_cpp.parse(bytes(self.concepts[concept][0][0], "utf-8")).root_node.sexp()
                elif input_language == PYTHON:
                    tree = parser_py.parse(bytes(self.concepts[concept][0][0], "utf-8")).root_node.sexp()
                lang_matches.append(tree)
                final_concept = process.extractOne(parse_tree, lang_matches, scorer=fuzz.partial_ratio)
                if final_concept[-1] >= 80:
                    concept_final = concept

        print(concept_final + " has the highest posssibility of being a correct match. Suggestion for optimized code is in suggestion.txt")
        with open('suggestion.txt', 'w') as datas:
            concept_string = concept_final[:-3]
            concept_string_py = concept_string + "_py"
            concept_string_jv = concept_string + "_jv"
            concept_string_cpp = concept_string + "_cpp"

            datas.write("PYTHON:\n")
            datas.write(str(self.concepts[concept_string_py][0][0])+"\n")
            datas.write("---------------------------------------------\n")
            datas.write("JAVA:\n")
            datas.write(str(self.concepts[concept_string_jv][0][0])+"\n")
            datas.write("---------------------------------------------\n")
            datas.write("CPP:\n")
            datas.write(str(self.concepts[concept_string_cpp][0][0]))


def create_parse_tree(input_code, input_language):
    """return s-expression and parse tree for the given code and language using the tree-sitter"""
    if input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8")).root_node.sexp()
    if input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8")).root_node.sexp()
    return parser_py.parse(bytes(input_code, "utf-8")).root_node.sexp()



concepts = Concept()

quanching = "name = [1,3,5,7,9]\nname.sort()"

concepts.check_similarity(quanching, PYTHON)
