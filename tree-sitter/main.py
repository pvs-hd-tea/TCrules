import parser

rule_set = parser.RuleSet()
rule_set.complete_simple_rules()

# added for better/ faster testing
while True: 
    user_code = str(input("Please enter a code to be translated or enter 'exit': "))
    if user_code == "exit":
        break
    user_code_language = str(input("Please enter the programming language the code above is written in: ")).upper()
    while user_code_language not in [parser.PYTHON, parser.JAVA, parser.CPP]:
        user_code_language = str(input("Please enter correct programming language: ")).upper()

    parse_tree, input_code, tree = parser.create_parse_tree(user_code, user_code_language)
    
    rule_found, rule_name = rule_set.rule_match(parse_tree, True)
    if rule_found:    
        translations = rule_set.translate(input_code, rule_name)
        print("PYTHON: " + translations[0])
        print("JAVA: " + translations[1])
        print("CPP: " + translations[2])
    else: 
        print(f"No appropriate rule for translating '{user_code}' was found in the database...")
        if str(input(f"Do you want to add rule for it? ")).upper() == "YES":

            if user_code_language.upper() == parser.JAVA:
                line_jv = user_code
                line_py = str(input(f"Please enter the aquivalent for '{line_jv}' in Python: "))
                line_cpp = str(input(f"Please enter the aquivalent for '{line_jv}' in C++: "))
            elif user_code_language.upper() == parser.PYTHON:
                line_py = user_code
                line_jv = str(input(f"Please enter the aquivalent for '{line_py}' in Java: "))
                line_cpp = str(input(f"Please enter the aquivalent for '{line_py}' in C++: "))
            else:
                line_cpp = user_code
                line_jv = str(input(f"Please enter the aquivalent for '{line_cpp}' in Java: "))
                line_python = str(input(f"Please enter the aquivalent for '{line_cpp}' in Python: "))

            rule_name = str(input(f"Please enter the rule name for '{line_cpp}': "))
            while rule_name in rule_set.parse_tree_dict:
                rule_name = str(input("This name is already in the database... Please enter another one: "))
            rule_set.add_rule(line_py, line_jv, line_cpp, rule_name)


rule_set.save_parse_tree_dict()