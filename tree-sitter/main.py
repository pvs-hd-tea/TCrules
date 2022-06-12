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

    parse_tree, input_code = parser.create_parse_tree(user_code, user_code_language)
    rule_found, rule_name = rule_set.rule_match(parse_tree, True)
    if rule_found:    
        translations = rule_set.translate(input_code, rule_name)
        print("PYTHON: " + translations[0])
        print("JAVA: " + translations[1])
        print("CPP: " + translations[2])
    else: 
        print(f"No appropriate rule for translating '{user_code}' was found in the database...")

rule_set.save_parse_tree_dict()