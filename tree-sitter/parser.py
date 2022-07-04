from ast import keyword
import os
from tree_sitter import Language, Parser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import json

function_names = ["incr"]
PYTHON = "PYTHON"
JAVA = "JAVA"
CPP = "CPP"

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

types = ["int", "float", "double", "boolean", "bool"]

operators = [["==", "!=", ">=", "<=", ">", "<"], # comparison
            ["++", "+=", "+", "--", "-=","-", "//", "/=", "/", "%=", "%", "**", "*=", "*"], # arithmetic and assignment
            ["&&", "||", "!", "and", "or", "not"], # logical
            ["is not", "is"], # identity
            ["not in", "in"] # membership
            ]

"""Create Parser"""
parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)

parser_jv = Parser()
parser_jv.set_language(JV_LANGUAGE)

parser_cpp = Parser()
parser_cpp.set_language(CPP_LANGUAGE)


class RuleSet:
    # Initializing
    def __init__(self):
        self.parse_tree_dict = {}
        if not os.path.isfile("rule-set.json"):
            self.create_parse_tree_dict()
        else:
            with open("rule-set.json") as file:
                self.parse_tree_dict = json.load(file)
                print(f"Loading the Rule Set ... Done ... Its length is {len(self.parse_tree_dict)}")
        with open("../own-parser-approach/keywords.json") as file:
                self.keywords = json.load(file)

    # Destructor
    """def __del__(self):
        with open("rule-set.json", "w+") as file:
            json.dump(self.parse_tree_dict, file, indent=4)
        #self.save_parse_tree_dict() # or create a separate function"""

    def create_parse_tree_dict(self):
        ''''predefine basic rule'''
        self.parse_tree_dict = {"ALLOCATION": {parser_py.parse(bytes("b = 5", "utf-8")).root_node.sexp(): "name = value",
                                               parser_jv.parse(bytes("int b = 5;", "utf-8")).root_node.sexp(): "type name = value;",
                                               parser_cpp.parse(bytes("int b = 5;", "utf-8")).root_node.sexp(): "type name = value;"
                                               },
                                "add_short": {parser_py.parse(bytes("b += 1", "utf-8")).root_node.sexp(): "name += value",
                                               parser_jv.parse(bytes("b++;", "utf-8")).root_node.sexp(): "nameoperator;",
                                               parser_cpp.parse(bytes("b++;", "utf-8")).root_node.sexp(): "nameoperator;"
                                               },
                                "sub_short": {parser_py.parse(bytes("b -= 1", "utf-8")).root_node.sexp(): "name -= value",
                                               parser_jv.parse(bytes("b--;", "utf-8")).root_node.sexp(): "nameoperator;",
                                               parser_cpp.parse(bytes("b--;", "utf-8")).root_node.sexp(): "nameoperator;"
                                               }
                                
                                }

    def save_parse_tree_dict(self):
        with open("rule-set.json", "w+") as file:
            json.dump(self.parse_tree_dict, file, indent=4)

    def create_generic_code_expression(self, code):
        generic_code = code

        names = return_name(code)
        if names:
            for name in names:
                #generic_code = generic_code.replace(name[0], "name", name[1])
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

        print(generic_code, code)
        return generic_code

    def add_rule(self, py_code, jv_code, cpp_code, rule_name):
        generic_py_code = self.create_generic_code_expression(py_code)
        generic_jv_code = self.create_generic_code_expression(jv_code)
        generic_cpp_code = self.create_generic_code_expression(cpp_code)

        self.parse_tree_dict.update({rule_name: {parser_py.parse(bytes(py_code, "utf-8")).root_node.sexp(): generic_py_code,
                                                 parser_jv.parse(bytes(jv_code, "utf-8")).root_node.sexp(): generic_jv_code,
                                                 parser_cpp.parse(bytes(cpp_code, "utf-8")).root_node.sexp(): generic_cpp_code
                                                 }
                                     })

    def complete_simple_rules(self):
        '''read parallel corpus and derive rules'''
        for func_name in function_names:
            with open("data/"+func_name+".py", 'r') as py, open("data/"+func_name+".java", 'r') as jv, open("data/"+func_name+".cpp", "r") as cpp:
                for line_py, line_jv, line_cpp in zip(py, jv, cpp):
                    parse_tree, input_code,_ = create_parse_tree(line_jv, JAVA)
                    if self.rule_match(parse_tree)[0]:
                        continue
                    rule_name = str(
                        input(f"Please enter the rule name for '{input_code[:-1]}': "))
                    while rule_name in self.parse_tree_dict:
                        rule_name = str(
                            input("This name is already in the database... Please enter another one: "))
                    self.add_rule(line_py, line_jv, line_cpp, rule_name)

    def rule_match(self, input_parse_tree, translate=False):
        ratio = []
        for rule_name in self.parse_tree_dict:
            temp = []
            for sexp_tree in self.parse_tree_dict[rule_name]:
                temp.append(fuzz.ratio(sexp_tree, input_parse_tree))
            ratio.append((max(temp), rule_name))
        ratios = [r[0] for r in ratio]
        max_ratio = max(ratios)
        #print(f"Rule match: {max_ratio}")
        if not translate:
            if max_ratio >= 96:
                return True, ratio[ratios.index(max_ratio)][1]
            return False, ""

        if max_ratio >= 88:
            return True, ratio[ratios.index(max_ratio)][1]
        return False, ""

    def translate(self, input_code, rule_name):
        '''translates the given input code by traversing available rules and replacing values, names, types and operators'''
        translations = []

        tokens = input_code.split()
        keywords = []
        tokens_to_replace = []
        for token in tokens:
            best_match = process.extractOne(token, self.keywords.keys(), scorer=fuzz.token_sort_ratio)
            if best_match[-1] == 100:
                keywords.append(self.keywords[best_match[0]])
                tokens_to_replace.append(token)
        print(tokens_to_replace)
        for i, sexp_tree in enumerate(self.parse_tree_dict[rule_name]):
            entry = self.parse_tree_dict[rule_name][sexp_tree]
            updated_input = input_code
            if keywords:
                for index, token in enumerate(tokens_to_replace):
                    if i == 0:
                        updated_input = re.sub(token, keywords[index]["python"], input_code)
                    elif i == 1:
                        updated_input = re.sub(token, keywords[index]["java"], input_code)
                    else:
                        updated_input = re.sub(token, keywords[index]["c++"], input_code)

            values = return_value(updated_input)
            if values:
                for value in values:
                    entry = entry.replace("value", value[0], value[1])           
        
            names = return_name(updated_input)
            if names:
                for name in names:
                    #entry = entry.replace("name", name[0], name[1])
                    entry = entry.replace("name", name, 1)

            type = return_type(updated_input)
            if type == "bool":
                best_match = process.extractOne("bool", self.keywords.keys(), scorer=fuzz.token_sort_ratio)
                if best_match[-1] == 100:
                    if i == 0:
                        entry = re.sub("type", self.keywords[best_match[0]]["python"], entry)
                    elif i == 1:
                        entry = re.sub("type", self.keywords[best_match[0]]["java"], entry)
                    else:
                        entry = re.sub("type", self.keywords[best_match[0]]["c++"], entry)
            elif type:
                entry = entry.replace("type", type) 
                    
            operator = return_operator(updated_input)
            if operator:
                entry = entry.replace("operator", operator)

            translations.append(entry)

        return translations


def create_parse_tree(input_code, input_language):
    '''creates a parse tree for given input code and input language'''
    if input_language == "PYTHON":
        return parser_py.parse(bytes(input_code, "utf-8")).root_node.sexp(), input_code, parser_py.parse(bytes(input_code, "utf-8"))
    elif input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8")).root_node.sexp(), input_code, parser_jv.parse(bytes(input_code, "utf-8"))
    elif input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8")).root_node.sexp(), input_code, parser_cpp.parse(bytes(input_code, "utf-8"))


def return_type(input_string):
    '''derive the type from the given string'''
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
    '''extract values from the given string'''
    numbers = re.findall(r'true|false|True|False', input_string)
    string = re.sub('([a-z,A-Z]+[_]*[a-z,A-Z,0-9]*)*', '', input_string)
    numbers.extend(re.findall(r'\d+(?:\.\d+)?', string))
    if numbers:
        #print("values",[(number, numbers.count(number)) for number in numbers])
        return [(number, numbers.count(number)) for number in numbers]


def return_name(input_string):
    '''extract the variable names in the given string'''
    string = re.sub('true|false|True|False', '', input_string)
    for type in types:
        string = string.replace(type, "")
    names = re.findall('([a-z,A-Z]+[_]*[a-z,A-Z,0-9]*)*', string)
    #names_count_list = [(name, names.count(name)) for name in names if name]
    #names_count_set = sorted(set(names_count_list), key=names_count_list.index)
    #print(names_count_set)
    #print([name for name in names if name])
    return [name for name in names if name]


def return_operator(input_string):
    '''extract the operator in the given string'''
    for i, group in enumerate(operators):
        for operator in group:
            if operator in input_string:
                #print("op", operator)
                return operator
    return None
