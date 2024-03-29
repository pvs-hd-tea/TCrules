import random
import string


cpp_types = ["int", "double", "float"]
java_types = ["int", "float", "double"]

EQUALS = "="

operators = ["+", "-", "*", "/"]

true_false_py = ["True", "False"]

true_false = ["true", "false"]

random_comparators = ["==", "<", ">"]


def create_random_bool_statement():
    random_boolean_statement = random.choice(string.ascii_lowercase) + random.choice(
        random_comparators) + random.choice(string.ascii_lowercase)
    return random_boolean_statement


def create_python_dataset():
<<<<<<< HEAD
    with open('data/big_eval_corpus/python_while_dataset.py','w',encoding="utf8") as f:
=======
    with open('data/big_eval_corpus/python_while_dataset.py', 'w') as f:
>>>>>>> 772e74b08209615d05cdebd0863542f1ce838eb3
        for i in range(1, 100):

            random_line_one = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))
            random_line_two = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))
            random_line_three = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))

            random_line_four = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))
            random_line_five = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))
            random_line_six = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))

            random_line_seven = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))
            random_line_eight = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))
            random_line_nine = random.choice(
                list(open('data/big_eval_corpus/python_assignment_dataset.py')))

            random_if_one = "if" + " " + create_random_bool_statement() + ":\n" + "     " + \
                random_line_one + "     " + random_line_two + "     " + random_line_three
            random_if_two = "if" + " " + create_random_bool_statement() + ":\n" + "     " + \
                random_line_four + "     " + random_line_five + "     " + random_line_six
            random_if_three = "if" + " " + create_random_bool_statement() + ":\n" + "     " + \
                random_line_seven + "     " + random_line_eight + "     " + random_line_nine

            f.write("while" + " " + create_random_bool_statement() + ":\n" +
                    "   " + random_if_one + "   " + random_if_two + "   " + random_if_three)


def create_java_dataset():

<<<<<<< HEAD
    with open('data/big_eval_corpus/java_while_dataset.java','w',encoding="utf8") as f:
=======
    with open('data/big_eval_corpus/java_while_dataset.java', 'w') as f:
>>>>>>> 772e74b08209615d05cdebd0863542f1ce838eb3
        for i in range(1, 100):
            random_line_one = random.choice(
                list(open('data/big_eval_corpus/java_assignment_dataset.java')))
            random_line_two = random.choice(
                list(open('data/big_eval_corpus/java_declaration_dataset.java')))
            random_line_three = random.choice(
                list(open('data/big_eval_corpus/java_assignment_dataset.java')))

            random_line_four = random.choice(
                list(open('data/big_eval_corpus/java_assignment_dataset.java')))
            random_line_five = random.choice(
                list(open('data/big_eval_corpus/java_declaration_dataset.java')))
            random_line_six = random.choice(
                list(open('data/big_eval_corpus/java_assignment_dataset.java')))

            random_line_seven = random.choice(
                list(open('data/big_eval_corpus/java_assignment_dataset.java')))
            random_line_eight = random.choice(
                list(open('data/big_eval_corpus/java_declaration_dataset.java')))
            random_line_nine = random.choice(
                list(open('data/big_eval_corpus/java_assignment_dataset.java')))

            random_if_one = "if" + " (" + create_random_bool_statement(
            ) + "){\n" + "     " + random_line_one + "     " + random_line_two + "     " + random_line_three + "}\n"
            random_if_two = "if" + " (" + create_random_bool_statement(
            ) + "){\n" + "     " + random_line_four + "     " + random_line_five + "     " + random_line_six + "}\n"
            random_if_three = "if" + " (" + create_random_bool_statement(
            ) + "){\n" + "     " + random_line_seven + "     " + random_line_eight + "     " + random_line_nine + "}\n"

            f.write("while" + " (" + create_random_bool_statement() +
                    "){\n" + "   " + random_if_one + "   " + random_if_two + "   " + random_if_three + "}\n")


def create_cpp_dataset():
<<<<<<< HEAD
    with open('data/big_eval_corpus/cpp_while_dataset.cpp','w',encoding="utf8") as f:
=======
    with open('data/big_eval_corpus/cpp_while_dataset.cpp', 'w') as f:
>>>>>>> 772e74b08209615d05cdebd0863542f1ce838eb3
        for i in range(1, 100):
            random_line_one = random.choice(
                list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp')))
            random_line_two = random.choice(
                list(open('data/big_eval_corpus/cpp_declaration_dataset.cpp')))
            random_line_three = random.choice(
                list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp')))

            random_line_four = random.choice(
                list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp')))
            random_line_five = random.choice(
                list(open('data/big_eval_corpus/cpp_declaration_dataset.cpp')))
            random_line_six = random.choice(
                list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp')))

            random_line_seven = random.choice(
                list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp')))
            random_line_eight = random.choice(
                list(open('data/big_eval_corpus/cpp_declaration_dataset.cpp')))
            random_line_nine = random.choice(
                list(open('data/big_eval_corpus/cpp_assignment_dataset.cpp')))

            random_if_one = "if" + " (" + create_random_bool_statement(
            ) + "){\n" + "     " + random_line_one + "     " + random_line_two + "     " + random_line_three + "}\n"
            random_if_two = "if" + " (" + create_random_bool_statement(
            ) + "){\n" + "     " + random_line_four + "     " + random_line_five + "     " + random_line_six + "}\n"
            random_if_three = "if" + " (" + create_random_bool_statement(
            ) + "){\n" + "     " + random_line_seven + "     " + random_line_eight + "     " + random_line_nine + "}\n"

            f.write("while" + " (" + create_random_bool_statement() +
                    "){\n" + "   " + random_if_one + "   " + random_if_two + "   " + random_if_three + "}\n")


create_python_dataset()
create_cpp_dataset()
create_java_dataset()
