import random
import string
import numpy


cpp_types = ["int", "double", "float"]
java_types = ["int", "float", "double"]

EQUALS = "="

operators = ["+", "-", "*", "/"]

true_false_py = ["True", "False"]

true_false = ["true", "false"]


def create_python_dataset():
    with open('../../test_files/python_declaration_dataset.py', 'w') as f:
        for i in range(1, 100):
            random_name = ''.join(random.choices(
                string.ascii_uppercase + string.ascii_lowercase, k=6))
            if numpy.random.choice([0, 1], p=[.8, .2]) == 0:
                random_number = str(random.choice(
                    [random.randint(1, 10000), random.uniform(1, 1000)]))
                f.write(random_name + " " + EQUALS +
                        " " + random_number + "\n")
            else:
                random_bool = random.choice(true_false_py)
                f.write(random_name + " " + EQUALS + " " + random_bool + "\n")


def create_java_dataset():

    with open('../../test_files/java_declaration_dataset.java', 'w') as f:
        for i in range(1, 100):
            random_name = ''.join(random.choices(
                string.ascii_uppercase + string.ascii_lowercase, k=6))
            random_type = random.choice(java_types)
            if numpy.random.choice([0, 1], p=[.8, .2]) == 0:
                if random_type == "int":
                    random_number = str(random.randint(1, 10000))
                    f.write(random_type + " " + random_name + " " +
                            EQUALS + " " + random_number + ";\n")
                else:
                    random_number = str(random.uniform(1, 1000))
                    f.write(random_type + " " + random_name + " " +
                            EQUALS + " " + random_number + ";\n")
            else:
                random_bool = random.choice(true_false)
                f.write("boolean" + " " + random_name + " " +
                        EQUALS + " " + random_bool + ";\n")


def create_cpp_dataset():
    with open('../../test_files/cpp_declaration_dataset.cpp', 'w') as f:
        for i in range(1, 100):
            random_name = ''.join(random.choices(
                string.ascii_uppercase + string.ascii_lowercase, k=6))
            random_type = random.choice(cpp_types)
            if numpy.random.choice([0, 1], p=[.8, .2]) == 0:
                if random_type == "int":
                    random_number = str(random.randint(1, 10000))
                    f.write(random_type + " " + random_name + " " +
                            EQUALS + " " + random_number + ";\n")
                else:
                    random_number = str(random.uniform(1, 1000))
                    f.write(random_type + " " + random_name + " " +
                            EQUALS + " " + random_number + ";\n")
            else:
                random_bool = random.choice(true_false)
                f.write("bool" + " " + random_name + " " +
                        EQUALS + " " + random_bool + ";\n")



create_python_dataset()
create_cpp_dataset()
create_java_dataset()
