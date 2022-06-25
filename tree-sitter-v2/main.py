from ast import arg
from tokenize import String
import parser
import logging
from argparse import ArgumentParser

logging.getLogger().setLevel(logging.ERROR)


if __name__ == "__main__":

    rule_set = parser.RuleSet()
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=str,
                            help="input file to translate. Has to be in same directory as TCR", metavar="FILE", required=True)
    arg_parser.add_argument("-i", "--inputlanguage",
                            choices=["CPP", "JAVA", "PYTHON"], required=True)
    arg_parser.add_argument("-o", "--outputlanguage",
                            choices=["CPP", "JAVA", "PYTHON"], required=True)

    arguments = arg_parser.parse_args()

    source_file = arguments.file

    input_language = arguments.inputlanguage
    output_language = arguments.outputlanguage

    if input_language == "JAVA" and output_language == "CPP":
        translations = rule_set.translate(source_file, parser.JAVA)
        print(f"\ntranslate from {parser.JAVA} ({len(translations)})")
        print("Output Language: " + output_language + "\n")
        for code_line in translations:
            print(code_line[1] + " ------------> " + code_line[0])

    if input_language == "CPP" and output_language == "JAVA":
        translations = rule_set.translate(source_file, parser.CPP)
        print(f"\ntranslate from {parser.CPP} ({len(translations)})")
        print("Output Language: " + output_language + "\n")
        for code_line in translations:
            print(code_line[0] + " ------------> " + code_line[1])

    if input_language == "PYTHON" and output_language == "CPP":
        translations = rule_set.translate(source_file, parser.PYTHON)
        print(f"\ntranslate from {parser.PYTHON} ({len(translations)})")
        print("Output Language: " + output_language + "\n")

        for code_line in translations:
            print(code_line[2] + " ------------> " + code_line[0])

    if input_language == "CPP" and output_language == "PYTHON":
        translations = rule_set.translate(source_file, parser.CPP)
        print(f"\ntranslate from {parser.CPP} ({len(translations)})")
        print("Output Language: " + output_language + "\n")
        for code_line in translations:
            print(code_line[0] + " ------------> " + code_line[2])

    if input_language == "PYTHON" and output_language == "JAVA":
        translations = rule_set.translate(source_file, parser.PYTHON)
        print(f"\ntranslate from {parser.PYTHON} ({len(translations)})")
        print("Output Language: " + output_language + "\n")
        for code_line in translations:
            print(code_line[2] + " ------------> " + code_line[1])

    if input_language == "JAVA" and output_language == "PYTHON":
        translations = rule_set.translate(source_file, parser.JAVA)
        print(f"\ntranslate from {parser.JAVA} ({len(translations)})")
        print("Output Language: " + output_language + "\n")
        for code_line in translations:
            print(code_line[1] + " ------------> " + code_line[2])

    if input_language == output_language:
        print("Input Language and output language are the same!")
