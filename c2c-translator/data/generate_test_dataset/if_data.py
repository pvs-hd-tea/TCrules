import random
import string


cpp_types = ["int", "double", "float"]
java_types = ["int", "float", "double"]

EQUALS = "="

operators = ["+", "-", "*", "/"]

true_false_py = ["True", "False"]

true_false = ["true", "false"]

random_comparators = ["==", "<" ,">"]


def create_random_bool_statement():
    random_boolean_statement = random.choice(string.ascii_lowercase) + random.choice(random_comparators) + random.choice(string.ascii_lowercase)
    return random_boolean_statement


def create_python_dataset():
    with open('../../test_corpus/python_if_dataset.py','w',encoding="utf8") as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('../../test_corpus/python_assignment_dataset.py',encoding="utf8")))
            random_line_two = random.choice(list(open('../../test_corpus/python_assignment_dataset.py',encoding="utf8")))
            random_line_three = random.choice(list(open('../../test_corpus/python_assignment_dataset.py',encoding="utf8")))
            f.write("if" + " " + create_random_bool_statement() + ":\n" + "   " + random_line_one + "   " + random_line_two + "   " + random_line_three)


def create_java_dataset():

    with open('../../test_corpus/java_if_dataset.java','w',encoding="utf8") as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('../../test_corpus/java_assignment_dataset.java',encoding="utf8")))
            random_line_two = random.choice(list(open('../../test_corpus/java_declaration_dataset.java',encoding="utf8")))
            random_line_three = random.choice(list(open('../../test_corpus/java_assignment_dataset.java',encoding="utf8")))
            f.write("if" + " (" + create_random_bool_statement() + "){\n" + "   " + random_line_one + "   " + random_line_two + "   " + random_line_three + "}\n")


def create_cpp_dataset():
    with open('../../test_corpus/cpp_if_dataset.cpp','w',encoding="utf8") as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('../../test_corpus/cpp_assignment_dataset.cpp',encoding="utf8")))
            random_line_two = random.choice(list(open('../../test_corpus/cpp_declaration_dataset.cpp',encoding="utf8")))
            random_line_three = random.choice(list(open('../../test_corpus/cpp_assignment_dataset.cpp',encoding="utf8")))
            f.write("if" + " (" + create_random_bool_statement() + "){\n" + "   " + random_line_one + "   " + random_line_two + "   " + random_line_three + "}\n")


create_python_dataset()
create_cpp_dataset()
create_java_dataset()
