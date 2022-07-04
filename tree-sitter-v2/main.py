import datetime
import parser
import logging
import re

from nbformat import write
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from argparse import ArgumentParser


logging.getLogger().setLevel(logging.ERROR)


rule_set = parser.RuleSet()

def translate(input_file, language, input_file_name):
    """translate the given input code and store the translations in separate files"""
    translations = rule_set.translate(input_file, language)

    file_end = [".cpp", ".java", ".py"]

    for i in range(3):
        with open("data/translations/translation_"+input_file_name+"_from_"+language.lower()+file_end[i], "a+", encoding="utf8") as file:
            file.truncate(0)
            file.seek(0)
            for code_line in translations:
                file.write(code_line[i])


def evaluate_translations(ground_truth, translations):
    """call evaluation on the given ground truth and translation"""
    for source, translation in zip(ground_truth, translations):
        calculate_metrics(source, translation)


def calculate_metrics(input_file, translation_file, write_eval_in_file=False):
    """calculate precision score of the translation of given input code"""
    with open(input_file, "r", encoding="utf8") as source, open(translation_file, "r", encoding="utf8") as translation:
        lines_source = source.readlines()
        lines_translation = translation.readlines()

    total_lines = len([line for line in lines_source if line != "\n"])
    correct = 0 # count correct translations
    i = 0 # track relevant lines

    for line_source in lines_source:
        if line_source != "\n": # non-empty line
            if i < len(lines_translation) and line_source == lines_translation[i]:
                correct += 1
            i += 1

    precision = correct / total_lines
    if write_eval_in_file:
        with open("data/translations/eval.txt", "a+", encoding="utf8") as evaluation:
            evaluation.write(datetime.datetime.now().strftime("%Y/%m/%d")+"\n\n")
            evaluation.write("Source: " + input_file + "\nTranslation: " + translation_file + "\n")
            evaluation.write("Precision: " + str(precision*100) + "\n")
            evaluation.write("________________________________________\n\n")
    else:
        print("\nSource: " + input_file + "\nTranslation: " + translation_file)
        print("Precision: " + str(precision*100))



if __name__ == "__main__":

    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=str,
                            help="input file to be translated", metavar="FILE", required=True)
    arg_parser.add_argument("-i", "--inputlanguage", choices=["CPP","JAVA","PYTHON"], required=True)
    arg_parser.add_argument("-o", "--outputlanguage", choices=["CPP","JAVA","PYTHON"], required=False)

    arguments = arg_parser.parse_args()
    source_file = arguments.file
    input_language = arguments.inputlanguage
    output_language = arguments.outputlanguage

    if input_language == output_language:
        print("Input Language and output language are the same!")

    else:
        input_language = process.extractOne(input_language,
                    [parser.CPP, parser.JAVA, parser.PYTHON], scorer=fuzz.ratio)[0]

        file_name = re.sub(r"([\w,-]*)(\.[a-z]*)", r"\1", source_file)

        ground_truth_files = [file_name + type for type in [".cpp",".java",".py"]]
        translation_files = ["data/translations/translation_"+file_name+"_from_"+input_language.lower()+type for type in [".cpp",".java",".py"]]

        translate(source_file, input_language, file_name)
        evaluate_translations(ground_truth_files, translation_files)
