from dis import code_info
import os
from tabnanny import check
from tree_sitter import Language, Parser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import json

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

PYTHON = "PYTHON"
JAVA = "JAVA"
CPP = "CPP"

#tree_keywords = ["assignment_expression", "expression_statement", "assignment","local_variable_declaration","declaration"]

types = ["int", "float", "double", "boolean", "bool"]

operators = [["==", "!=", ">=", "<=", ">", "<"], # comparison
            ["++", "+=", "+", "--", "-=","-", "//", "/=", "/", "%=", "%", "**", "*=", "*"], # arithmetic and assignment
            ["&&", "||", "!", "and", "or", "not"], # logical
            ["is not", "is"], # identity
            ["not in", "in"] # membership
            ]

files = ["simple"]

"""Create Parser"""
parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)

parser_jv = Parser()
parser_jv.set_language(JV_LANGUAGE)

parser_cpp = Parser()
parser_cpp.set_language(CPP_LANGUAGE)


class RuleSet:
    def __init__(self):
        if not os.path.isfile("rules.json"):
            self.rules = {}
        else:
            with open("rules.json") as file:
                self.rules = json.load(file)
                print(f"Loading {len(self.rules)} rules ... Done ...")    
        
        with open("../own-parser-approach/keywords.json") as file:
            self.keywords = json.load(file)

        if not os.path.isfile("tree-keywords.txt"):
            self.tree_keywords = []
        else:
            with open("tree-keywords.txt") as file:
                self.tree_keywords = file.read().split(",")
                print(f"Loading {len(self.tree_keywords)} keywords for parse tree ... Done ...")  

    def save_rules(self):
        with open("rules.json", "a+") as file:
            json.dump(self.rules, file, indent=4)

    def save_keywords(self):
        with open("tree-keywords.txt", "a+") as file:
            file.truncate(0)
            file.seek(0)
            length = len(self.tree_keywords)-1
            if length>0:
                for i, item in enumerate(self.tree_keywords):
                    if i == length:
                        file.write(item)
                    else:
                        file.write(item+",")
            else:
                file.write(self.tree_keywords[0])

    def check_for_keyword(self, parse_tree_sexp, parse_tree):
        for keyword in self.tree_keywords:
            if keyword in parse_tree_sexp:
                return keyword
        
        root_node = parse_tree.root_node
        self.tree_keywords.append(root_node.children[0].type)
        return str(root_node.children[0].type)


    def create_generic_expression(self, code):
        generic_code = code

        names = return_name(code)
        if names:
            for name in names:
                generic_code = generic_code.replace(name, "name", 1)

        values = return_value(code)
        if values:
            for value in values:
                generic_code = generic_code.replace(
                    value[0], "value", value[1])
        
        type = return_type(code)
        if type:
            generic_code = generic_code.replace(type, "type")

        operator = return_operator(code)
        if operator:
            generic_code = generic_code.replace(operator, "operator")

        #print(generic_code, code)
        return generic_code


    def extend_rule(self, cpp, jv, py, key):
        generic_cpp = self.create_generic_expression(cpp)
        generic_jv = self.create_generic_expression(jv)
        generic_py = self.create_generic_expression(py)

        flag = False

        for list in self.rules[key]:
            if generic_cpp in list:
                flag = True 
        if flag == False:
            self.rules[key].append([generic_cpp, generic_jv, generic_py])
        #print(self.rules)


    def add_rule(self, cpp, jv, py, key):
        generic_cpp = self.create_generic_expression(cpp)
        generic_jv = self.create_generic_expression(jv)
        generic_py = self.create_generic_expression(py)

        self.rules.update({key: [[generic_cpp, generic_jv, generic_py]]})
        #print(self.rules)

    #in_brackets = re.sub(r"[\s,\w]*=\s([\w,\s]*)\n", r"(\1)", generic_py)

    def derive_rules(self, files):
        for file in files:
            with open("data/"+file+".py", 'r') as py, open("data/"+file+".java", 'r') as jv, open("data/"+file+".cpp", "r") as cpp:
                for line_py, line_jv, line_cpp in zip(py, jv, cpp):
                    tree_sexp, tree = create_parse_tree(line_jv, JAVA)
                    keyword = self.check_for_keyword(tree_sexp, tree)
                    if keyword:
                        best_match = process.extractOne(keyword, self.rules.keys(), scorer=fuzz.partial_ratio)
                        if not best_match or best_match[-1] != 100:
                            self.add_rule(line_cpp, line_jv, line_py, keyword)
                        else:
                            self.extend_rule(line_cpp, line_jv, line_py, best_match[0])

    def translate(self, file_name, language):
        translations = []
        with open("data/"+file_name, 'r') as file:
            for line in file:
                tree_sexp, tree = create_parse_tree(line, language)
                keyword = self.check_for_keyword(tree_sexp, tree)
                if keyword:
                    best_match = process.extractOne(keyword, self.rules.keys(), scorer=fuzz.partial_ratio)
                    if best_match[-1] == 100:
                        for list in self.rules[best_match[0]]:
                            if self.create_generic_expression(line) in list:
                                translations.append(self.transform(list, line))
                    else:
                        print(f"No appropriate rule was found in the database...")
            return translations

    def transform(self, generic_expressions, code):
        translations = []

        tokens = code.split()
        keywords = []
        tokens_to_replace = []
        for token in tokens:
            best_match = process.extractOne(token, self.keywords.keys(), scorer=fuzz.token_sort_ratio)
            if best_match[-1] == 100:
                keywords.append(self.keywords[best_match[0]])
                tokens_to_replace.append(token)
        
        for i, entry in enumerate(generic_expressions):
            updated_input = code
            if keywords:
                for index, token in enumerate(tokens_to_replace):
                    if i == 0:
                        updated_input = re.sub(token, keywords[index]["c++"], updated_input)
                    elif i == 1:
                        updated_input = re.sub(token, keywords[index]["java"], updated_input)
                    else:
                        updated_input = re.sub(token, keywords[index]["python"], updated_input)

            values = return_value(updated_input)
            if values:
                for value in values:
                    entry = entry.replace("value", value[0], value[1])           
        
            names = return_name(updated_input)
            if names:
                for name in names:
                    entry = entry.replace("name", name, 1)

            type = return_type(updated_input)
            if type == "bool":
                best_match = process.extractOne("bool", self.keywords.keys(), scorer=fuzz.token_sort_ratio)
                if best_match[-1] == 100:
                    if i == 0:
                        entry = re.sub("type", self.keywords[best_match[0]]["c++"], entry)
                    elif i == 1:
                        entry = re.sub("type", self.keywords[best_match[0]]["java"], entry)
                    else:
                        entry = re.sub("type", self.keywords[best_match[0]]["python"], entry)
            elif type:
                entry = entry.replace("type", type) 
                    
            operator = return_operator(updated_input)
            if operator:
                entry = entry.replace("operator", operator)

            translations.append(entry)

        return translations



def create_parse_tree(input_code, input_language):
    if input_language == "PYTHON":
        return parser_py.parse(bytes(input_code, "utf-8")).root_node.sexp(), parser_py.parse(bytes(input_code, "utf-8"))
    elif input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8")).root_node.sexp(), parser_jv.parse(bytes(input_code, "utf-8"))
    elif input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8")).root_node.sexp(), parser_cpp.parse(bytes(input_code, "utf-8"))


def return_type(input_string):
    for type in types:
        if type in input_string:
            return type

    numbers = return_value(input_string)
    if numbers and len(numbers) == 1:
        if numbers[0][0] in ["true", "false", "True", "False"]:
            return "bool"
        if re.search(r"\.", numbers[0][0]) is None:
            return "int"
        elif len(numbers[0][0]) < 9:
            return "float"  # 6-7 significant digits
        return "double"  # 15-16 significant digits

    if numbers:  # more than one
        flag_float, flag_double = False, False
        for number in numbers:
            if number in ["true", "false", "True", "False"]:
                return "bool"
            if re.search(r"\.", number[0]) is None:
                continue  # int
            elif len(number[0]) < 9:
                flag_float = True  # 6-7 significant digits
            else:
                flag_double = True  # 15-16 significant digits
        if flag_double:
            return "double"
        if flag_float:
            return "float"
        return "int"
    return None


def return_value(input_string):
    numbers = re.findall(r'true|false|True|False', input_string)
    string = re.sub('([a-z,A-Z]+[_]*[a-z,A-Z,0-9]*)*', '', input_string)
    numbers.extend(re.findall(r'\d+(?:\.\d+)?', string))
    if numbers:
        #print("values",[(number, numbers.count(number)) for number in numbers])
        return [(number, numbers.count(number)) for number in numbers]


def return_name(input_string):
    string = re.sub('true|false|True|False', '', input_string)
    for type in types:
        string = string.replace(type, "")
    names = re.findall('([a-z,A-Z]+[_]*[a-z,A-Z,0-9]*)*', string)
    #print([name for name in names if name])
    return [name for name in names if name]


def return_operator(input_string):
    for i, group in enumerate(operators):
        for operator in group:
            if operator in input_string:
                #print("op", operator)
                return operator
    return None


