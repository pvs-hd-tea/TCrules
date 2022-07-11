import parser
from argparse import ArgumentParser

rule_set = parser.RuleSet()
arg_parser = ArgumentParser()

arg_parser = ArgumentParser()
arg_parser.add_argument("-f", "--file", type=str,
                            help="input file to be translated", metavar="FILE", required=True)
arg_parser.add_argument("-i", "--inputlanguage", choices=["CPP","JAVA","PYTHON"], required=True)

arguments = arg_parser.parse_args()
source_file = arguments.file
input_language = arguments.inputlanguage

translation = rule_set.translate(source_file,input_language)