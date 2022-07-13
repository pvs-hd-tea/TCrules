import parser
from argparse import ArgumentParser


TRANSLATE_FLAG = False

rule_set = parser.RuleSet()
arg_parser = ArgumentParser()

arg_parser = ArgumentParser()
arg_parser.add_argument("-f", "--file", type=str,
                            help="input file to be translated", metavar="FILE", required=False)
arg_parser.add_argument("-i", "--inputlanguage", choices=["CPP","JAVA","PYTHON"], required=False)

arguments = arg_parser.parse_args()
source_file = arguments.file
input_language = arguments.inputlanguage


if TRANSLATE_FLAG: # translate given file
    translations = rule_set.translate(source_file, input_language)
    for code_line in translations:
        print(code_line)

else: # derive rules from parallel corpus
    rule_set.derive_rules(parser.files)
    rule_set.save_rules()

rule_set.save_keywords()
