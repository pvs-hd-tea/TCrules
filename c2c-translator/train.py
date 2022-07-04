import parser

rule_set = parser.RuleSet()

TRANSLATE_FLAG = False

if TRANSLATE_FLAG:
    translations = rule_set.translate("data/test_files/test.cpp", parser.CPP)
    print(f"\ntranslate from {parser.CPP} ({len(translations)})\n")
    for code_line in translations:
        print(code_line)

    translations = rule_set.translate("data/test_files/test.java", parser.JAVA)
    print(f"\ntranslate from {parser.JAVA} ({len(translations)})\n")
    for code_line in translations:
        print(code_line)

    translations = rule_set.translate("data/test_files/test.py", parser.PYTHON)
    print(f"\ntranslate from {parser.PYTHON} ({len(translations)})\n")
    for code_line in translations:
        print(code_line)

else:
    rule_set.derive_rules(parser.files)
    rule_set.save_rules()

rule_set.save_keywords()
