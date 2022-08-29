import parser
import time


if __name__ == "__main__":

    rule_set = parser.RuleSet()
    input_code = "a = 5.5;"
    input_file = "data/test_corpus/cpp/simple.cpp"
    input_language = parser.CPP
    languages = [parser.CPP, parser.JAVA, parser.PYTHON]

    print("\n1) Translations from single code line:")
    print(f"\nInput code: {input_code}\nInput language: {input_language}\n")

    time.sleep(1)

    translations,_ = rule_set.translate_line(input_code, input_language)
    for i, translation in enumerate(translations):
        print(f"{languages[i]}: {translation}")

    time.sleep(1)

    translations = rule_set.translate_file(input_file, input_language)
    print(f"\n2) Translations from source file ({input_file}):")

    time.sleep(1)

    if len(translations) > 1: # multiple parts
        zipped = zip(*translations)
        for i, element in enumerate(zipped):
            print("\n\n"+languages[i]+"\n___________")
            for line in element:
                print(line[:-1])
            time.sleep(1)
    else:
        for i in range(3):
            print("\n\n"+languages[i]+"\n___________")
            for line in translations:
                print(line)
            time.sleep(1)
