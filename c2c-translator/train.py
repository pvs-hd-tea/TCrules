import parser
from argparse import ArgumentParser


rule_set = parser.RuleSet()
arg_parser = ArgumentParser()

arg_parser = ArgumentParser()
arg_parser.add_argument("-f", "--file", type=str,
                        help="input file to be translated", metavar="FILE", required=False)
arg_parser.add_argument("-i", "--inputlanguage",
                        choices=["CPP", "JAVA", "PYTHON"], required=False)
arg_parser.add_argument("-tn", "--train",
                        metavar="TRAIN", help="train parser", required=False)
arg_parser.add_argument("-t","--translate", required=False)

arguments = arg_parser.parse_args()
source_file = arguments.file
input_language = arguments.inputlanguage
training = arguments.train
translate = arguments.translate

if training:
    rule_set.derive_rules(parser.files)
    rule_set.save_rules()

if translate:  # translate given file
    translations = rule_set.translate(source_file, input_language)
    for code_line in translations:
        print(code_line)

rule_set.save_keywords()
