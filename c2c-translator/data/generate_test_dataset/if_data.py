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
<<<<<<< HEAD
    with open('data/big_eval_corpus/python_if_dataset.py','w',encoding="utf8") as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('data/big_eval_corpus/python_assignment_dataset.py',encoding="utf8")))
            random_line_two = random.choice(list(open('data/big_eval_corpus/python_assignment_dataset.py',encoding="utf8")))
            random_line_three = random.choice(list(open('data/big_eval_corpus/python_assignment_dataset.py',encoding="utf8")))
=======
    with open('data/big_eval_corpus/python_if_dataset.py', 'w') as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('data/big_eval_corpus/python_assignment_dataset.py')))
            random_line_two = random.choice(list(open('data/big_eval_corpus/python_assignment_dataset.py')))
            random_line_three = random.choice(list(open('data/big_eval_corpus/python_assignment_dataset.py')))
>>>>>>> 772e74b08209615d05cdebd0863542f1ce838eb3
            f.write("if" + " " + create_random_bool_statement() + ":\n" + "   " + random_line_one + "   " + random_line_two + "   " + random_line_three)


def create_java_dataset():

<<<<<<< HEAD
    with open('data/big_eval_corpus/java_if_dataset.java','w',encoding="utf8") as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('data/big_eval_corpus/java_assignment_dataset.java',encoding="utf8")))
            random_line_two = random.choice(list(open('data/big_eval_corpus/java_declaration_dataset.java',encoding="utf8")))
            random_line_three = random.choice(list(open('data/big_eval_corpus/java_assignment_dataset.java',encoding="utf8")))
=======
    with open('data/big_eval_corpus/java_if_dataset.java', 'w') as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('data/big_eval_corpus/java_assignment_dataset.java')))
            random_line_two = random.choice(list(open('data/big_eval_corpus/java_declaration_dataset.java')))
            random_line_three = random.choice(list(open('data/big_eval_corpus/java_assignment_dataset.java')))
>>>>>>> 772e74b08209615d05cdebd0863542f1ce838eb3
            f.write("if" + " (" + create_random_bool_statement() + "){\n" + "   " + random_line_one + "   " + random_line_two + "   " + random_line_three + "}\n")


def create_cpp_dataset():
<<<<<<< HEAD
    with open('data/big_eval_corpus/cpp_if_dataset.cpp','w',encoding="utf8") as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp',encoding="utf8")))
            random_line_two = random.choice(list(open('data/big_eval_corpus/cpp_declaration_dataset.cpp',encoding="utf8")))
            random_line_three = random.choice(list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp',encoding="utf8")))
=======
    with open('data/big_eval_corpus/cpp_if_dataset.cpp', 'w') as f:
        for i in range(1, 100):
            random_line_one = random.choice(list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp')))
            random_line_two = random.choice(list(open('data/big_eval_corpus/cpp_declaration_dataset.cpp')))
            random_line_three = random.choice(list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp')))
>>>>>>> 772e74b08209615d05cdebd0863542f1ce838eb3
            f.write("if" + " (" + create_random_bool_statement() + "){\n" + "   " + random_line_one + "   " + random_line_two + "   " + random_line_three + "}\n")


create_python_dataset()
create_cpp_dataset()
create_java_dataset()
