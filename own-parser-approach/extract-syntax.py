import itertools
import string
import token
import tokenize
import keyword
import re
import json
#import spacy
from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
#import Levenshtein as lev

JSON_DICT_FILE_NAME = "rules.json"

keywords = []
names = []
numbers = []
op = []

# to be extended, maybe differ between type of variable and type of function ?
types_cplusplus = ["boolean", "char", "int", "float","double", "short", "long", "std::string", "void"]
types_java = ["boolean", "char", "int", "float","double", "short", "long", "String", "void", "byte", "static", "public"]


def create_txt(file_name, file_name_txt, language):
    """ creates generalized txt from source code """
    with open(file_name) as f:
        if language == "java":
            types = types_java
        else:
            types = types_cplusplus
        
        names_text = [token.string for token in names]
        language_txt = open(file_name_txt, "w")
        
        for line in f:
            for type in types:
                if type in line:
                    if language == "java" and (type == "static" or type == "public"):
                        line = re.sub(rf"{type}", "", line) # omit them 
                    else: 
                        line = re.sub(rf"{type}", " type", line) # replace them wiht " type"

            # add spaces if there are not any to separate tokens
            line = re.sub(r"(\w)([(|{|;|)|}])", r"\1 \2", line)
            line = re.sub(r"(\S)([\n])", r"\1 \2", line)
            line = line.lstrip() # remove leading tabs

            tokens = line.split()
            for token in tokens:
                if token in names_text:
                    line = re.sub(rf"\s?{token}", " name", line) # replace any variable parts with "name"
            
            language_txt.write(line)
        
        language_txt.close()


def analyze_python_code(file_name_py, file_name_txt):
    """ creates generalized txt file from source code and stores tokens """
    with open(file_name_py) as file_py:
        tokens = tokenize.generate_tokens(file_py.readline)
        #print([token.string for token in tokens])
        file_txt = open(file_name_txt, "w")
        line = []
        for t in tokens:
            if t.type == 1: # NAME (token.tok_name[t.type])
                if keyword.iskeyword(t.string):
                    if t.string == "def": # def in python --> type in java and c++
                        line.append("type")
                        keywords.append(t)
                        continue
                    keywords.append(t)
                else: 
                    line.append("name") # variable part
                    names.append(t)
                    continue

            elif t.type == 54: # OP
                op.append(t)
                if t.string == "=": # add type for java and c++
                    temp = line[-1]
                    line[-1] = "type"
                    line.append(temp)
                if t.string == ")" and line[-1] == "(":
                    line[-1] = "()"
                    continue

            elif t.type == 2: # NUMBER
                numbers.append(t)

            elif t.type == 4: # NEWLINE
                line.append(t.string)
                file_txt.write(" ".join(line))
                line = []
                continue

            elif t.type in [0,5,6]: # INDENT, DEDENT or ENDMARKER
                continue
            else: 
                print("not stored:", t.string, t.type, token.tok_name[t.type])

            line.append(t.string)
        file_txt.close()

# does not work well!
def jaccard_similarity(x,y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def find_similarities():
    """ looks for similar lines of code """
    analyze_python_code("hello.py", "python.txt") # first python in order to get keywords, names etc. (variable and const code parts)
    
    print("keywords",[keyword.string for keyword in keywords]) # python keywords
    print("names", [name.string for name in names]) # identifier
    print("numbers", [number.string for number in numbers]) # numeric literal
    print("operators", [o.string for o in op]) # operators, delimiters, and the ellipsis literal

    create_txt("hello.cpp", "cpp.txt", "cpp")
    create_txt("hello.java", "java.txt", "java")

    # TODO:
    # find matching rows (better function eg. fuzzy)
    with open("python.txt", "r+") as f1, open("cpp.txt", "r+") as f2:
        similar_lines = []
        for x, y in itertools.product(f1,f2):
            lines = [line.lower().split(" ") for line in [x, y]]
            ratio = fuzz.partial_ratio(" ".join(lines[0]), " ".join(lines[1]))
            ratio2 = fuzz.ratio(" ".join(lines[0]), " ".join(lines[1]))
            if ratio > 90:
                similar_lines.append([ratio, lines[0], lines[1]])
        return similar_lines

# TODO
# in case of matching, devide rules and add them in the dich with rules
def derive_rules(matchings, db_dict):
    python_keywords = [keyword.string for keyword in keywords]
    for match in matchings:
        for token1 in match[1]:
            for token2 in match[2]:
                if fuzz.ratio(token1, token2) > 90:
                    if token1 in python_keywords and token1 not in db_dict.keys():
                        db_dict[token1] = {"cpp": token2, "python": token1}
    
def read_from_json(json_file):
    """ reads json file into dictionary """
    with open(json_file, 'r') as f:
        return json.load(f)


def write_to_dict(db_dict, json_file):
    """ writes dictionary into json file"""
    json_object = json.dumps(db_dict, indent = 4)
    with open(json_file, "w") as f:
        f.write(json_object)


db_dict = read_from_json(JSON_DICT_FILE_NAME)
similar_lines = find_similarities()
derive_rules(similar_lines, db_dict)
write_to_dict(db_dict, JSON_DICT_FILE_NAME)
            
    