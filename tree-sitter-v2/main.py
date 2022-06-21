import parser


if __name__ == "__main__":
    rule_set = parser.RuleSet()

    #rule_set.derive_rules(parser.files)

    translations = rule_set.translate("simple.cpp", parser.CPP)
    for code_line in translations:
        print(code_line)


    #rule_set.save_rules()

    rule_set.save_keywords()

    """input_code = str(input("Input code: "))
    input_language = str(input("Input language: ")).upper()
    tree = create_parse_tree(input_code, input_language)
    type = check_for_keyword(tree)
    num = re.findall(r'\d+', input_code)
    print(type + "(" + num[0] + ")")"""
