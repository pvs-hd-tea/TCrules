import parser
import concepts


if __name__ == "__main__":

    rule_set = parser.RuleSet()
    input_code = "a = 5.5"
    input_file = "data/test_corpus/python/simple.py"
    input_language = parser.PYTHON
    languages = [parser.CPP, parser.JAVA, parser.PYTHON]

    print("\n1) Translations from single code line:")
    print(f"\nInput code: {input_code}\nInput language: {input_language}\n")

    translations,_ = rule_set.translate_line(input_code, input_language)
    for i, translation in enumerate(translations):
        print(f"{languages[i]}: {translation}")

    translations = rule_set.translate_file(input_file, input_language)
    print(f"\n2) Translations from source file ({input_file}):")

    if len(translations) > 1: # multiple parts
        zipped = zip(*translations)
        for i, element in enumerate(zipped):
            print("\n\n"+languages[i]+"\n___________")
            for line in element:
                print(line[:-1])
    else:
        for i, translation in enumerate(translations[0]):
            print("\n\n"+languages[i]+"\n___________")
            print(translation)

    concept = concepts.Concept()
    input_code = "arr = [1,4,3,2,5]\narr.sort()"
    input_language = parser.PYTHON

    print("\n3) Translations from concept:")
    print(f"\nInput code:\n{input_code}\n\nInput language: {input_language}\n")

    concept.check_similarity(input_code,"PYTHON")
