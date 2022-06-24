import parser
import logging

logging.getLogger().setLevel(logging.ERROR)


if __name__ == "__main__":
    rule_set = parser.RuleSet()

    translate = False

    if translate: 
        translations = rule_set.translate("test.cpp", parser.CPP)
        print(f"\ntranslate from {parser.CPP} ({len(translations)})\n")
        for code_line in translations:
            print(code_line)

        translations = rule_set.translate("test.java", parser.JAVA)
        print(f"\ntranslate from {parser.JAVA} ({len(translations)})\n")
        for code_line in translations:
            print(code_line)

        translations = rule_set.translate("test.py", parser.PYTHON)
        print(f"\ntranslate from {parser.PYTHON} ({len(translations)})\n")
        for code_line in translations:
            print(code_line)

    else:
        rule_set.derive_rules(parser.files)
        rule_set.save_rules()

    rule_set.save_keywords()

    """input_code = str(input("Input code: "))
    input_language = str(input("Input language: ")).upper()
    tree = create_parse_tree(input_code, input_language)
    type = check_for_keyword(tree)
    num = re.findall(r'\d+', input_code)
    print(type + "(" + num[0] + ")")"""
