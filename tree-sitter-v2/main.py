import datetime
import parser
import logging
import re
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from argparse import ArgumentParser

logging.getLogger().setLevel(logging.ERROR)


rule_set = parser.RuleSet()

def translate(source_file, language):
    translations = rule_set.translate(source_file, language)

    with open("data/translations/translations.cpp", "a+") as file:
        file.truncate(0)
        file.seek(0)
        for code_line in translations:
            file.write(code_line[0])

    with open("data/translations/translations.java", "a+") as file:
        file.truncate(0)
        file.seek(0)
        for code_line in translations:
            file.write(code_line[1])

    with open("data/translations/translations.py", "a+") as file:
        file.truncate(0)
        file.seek(0)
        for code_line in translations:
            file.write(code_line[2])


def evaluate_translations(ground_truth_files, translation_files):
    for file, translation in zip(ground_truth_files, translation_files):
        calculate_metrics(file, translation)


def calculate_metrics(source_file, translation_file):
    with open(source_file, "r") as source, open(translation_file, "r") as translation:
        lines_source = source.readlines()
        lines_translation = translation.readlines()
    
    total_lines = len(lines_source)
    correct = 0
    i = 0

    for line_s in lines_source:
        if line_s != "\n":
            if line_s == lines_translation[i]:
                correct += 1
            i += 1
        else:
            correct += 1

    with open("data/translations/eval.txt", "a+") as eval:
        precision = correct / total_lines
        eval.write(datetime.datetime.now().strftime("%Y/%m/%d")+"\n\n")
        eval.write("Source: " + source_file + "\nTranslation: " + translation_file + "\n")
        eval.write("Precision: " + str(precision*100) + "\n")
        eval.write("________________________________________\n\n")

    

if __name__ == "__main__":

    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=str,
                            help="input file to translate. Has to be in same directory as TCR", metavar="FILE", required=True)
    arg_parser.add_argument("-i", "--inputlanguage", choices=["CPP", "JAVA", "PYTHON"], required=True)
    arg_parser.add_argument("-o", "--outputlanguage", choices=["CPP", "JAVA", "PYTHON"], required=False)

    arguments = arg_parser.parse_args()

    source_file = arguments.file

    input_language = arguments.inputlanguage
    output_language = arguments.outputlanguage

    if input_language == output_language:
        print("Input Language and output language are the same!")

    else: 
        language = process.extractOne(input_language, [parser.CPP, parser.JAVA, parser.PYTHON], scorer=fuzz.ratio)[0]
        translate(source_file, language)

        file_name = re.sub(r"([a-z,_,A-Z,0-9]*.)([a-z]*)", r"\1", source_file)
        ground_truth_files = ["data/"+file_name+type for type in ["cpp", "java", "py"]]
        translation_files = ["data/translations/translations."+type for type in ["cpp", "java", "py"]]
        
        evaluate_translations(ground_truth_files, translation_files)


    """if input_language == "JAVA" and output_language == "CPP":
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
            print(code_line[1] + " ------------> " + code_line[2])"""

