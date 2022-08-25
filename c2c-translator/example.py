import parser


if __name__ == "__main__":

    rule_set = parser.RuleSet()
    input_code = "a = 5.5"
    input_file = "data/test_corpus/python/simple.py"
    input_language = parser.PYTHON
    languages = [parser.CPP, parser.JAVA, parser.PYTHON]

    print(f"\nInput code: {input_code}\nInput language: {input_language}\nTranslating...")

    translations,_ = rule_set.translate_line(input_code, input_language)
    for i, translation in enumerate(translations):
        print(f"{languages[i]}: {translation}")

    translations = rule_set.translate_file(input_file, input_language)
    print(f"\nTranslations from {input_file}:")
    
    if len(translations) > 1: # multiple parts
        zipped = zip(*translations)
        for i, element in enumerate(zipped):
            print("\n\n"+languages[i]+"\n___________")
            for line in element:
                print(line[:-1])
    else:
        for line in translations:
            print(line)
