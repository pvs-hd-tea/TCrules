import parser

import datetime
import logging
import re

from argparse import ArgumentParser

logging.getLogger().setLevel(logging.ERROR)


rule_set = parser.RuleSet()

def translate(input_file, language, input_file_name):
    """translate the given input code and store the translations in separate files"""
    translations = rule_set.translate_file(input_file, language)

    file_end = [".cpp", ".java", ".py"]

    for i in range(3):
        with open("data/translations/" + input_file_name + "_from_" + language.lower() + file_end[i], "a+", encoding="utf8") as file:
            file.truncate(0)
            file.seek(0)

            for line in translations:
                file.write(line[i])


def evaluate_translations(ground_truth, translations, write_eval_in_file=False):
    """call evaluation on the given ground truth and translation"""
    with open("data/evaluation/wrong.txt","a+",encoding="utf8") as wrong:
        wrong.truncate(0)
        wrong.seek(0)
    
    for source, translation in zip(ground_truth, translations):
        calculate_metrics(source, translation, write_eval_in_file)


def calculate_metrics(input_file, translation_file, write_eval_in_file=False):
    """calculate precision score of the translation of given input code"""
    with open(input_file, "r", encoding="utf8") as source, open(translation_file, "r", encoding="utf8") as translation:
        lines_source = source.readlines()
        lines_translation = translation.readlines()

    with open("data/evaluation/wrong.txt","a+",encoding="utf8") as wrong:
        total_lines = len([line for line in lines_source if line != "\n"])
        correct = 0 # count correct translations
        i = 0 # track relevant lines

        if len(lines_source) >= len(lines_translation):
            for j,line_source in enumerate(lines_source):
                if line_source.lstrip() != "": # non-empty line
                    if i < len(lines_translation) and line_source.rstrip() == lines_translation[i].rstrip():
                        correct += 1
                    elif i < len(lines_translation):
                        if not write_eval_in_file:
                            print(f"wrong translation: {i,lines_translation[i]} of source: {j,line_source}")
                        else:
                            wrong.write(input_file + " vs. " + translation_file +"\n" + str(j)+")"+line_source+str(i)+")"+lines_translation[i]+"___________\n")
                    i += 1
        else:
            for j, line_translation in enumerate(lines_translation):
                if line_translation.lstrip() != "": # non-empty line
                    if i < len(lines_source) and line_translation.rstrip() == lines_source[i].rstrip():
                        correct += 1
                    elif i < len(lines_source):
                        if not write_eval_in_file:
                            print(f"wrong translation: {j,line_translation} of source: {i, lines_source[i]}")
                        else:
                            wrong.write(input_file + " vs. " + translation_file +"\n" + str(j)+")"+line_source+str(i)+")"+lines_translation[i]+"___________\n")
                    i += 1

        precision = correct / total_lines

        if write_eval_in_file:
            with open("data/evaluation/metrics.txt", "a+", encoding="utf8") as evaluation:
                evaluation.write(datetime.datetime.now().strftime("%Y/%m/%d")+"\n")
                evaluation.write("\nSource: " + input_file + "\nTranslation: " + translation_file + "\n")
                evaluation.write("Precision: " + str(precision*100) + "\n")
                evaluation.write("________________________________________\n\n")
        else:
            print(f"Source: {input_file} \nTranslation: {translation_file}")
            print(f"Precision: {precision*100}\n")


if __name__ == "__main__":

    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=str, help="input source code to be translated", metavar="FILE", required=True)
    arg_parser.add_argument("-l", "--language", help="input language to be translated from", choices=["cpp","java","python"], required=True)
    arg_parser.add_argument("-e", "--evaluation", help="store evaluation metrics in a separate file", choices=["True","False"], required=False)


    arguments = arg_parser.parse_args()
    source_file = arguments.file
    input_language = arguments.language.upper()

    file_name = re.sub(r"([\w,-]*)(\.[a-z]*)", r"\1", source_file)

    ground_truth_files = ["data/test_corpus/" + folder + file_name + ending for folder, ending in [("cpp/", ".cpp"),("java/", ".java"),("python/", ".py")]]
    translation_files = ["data/translations/" + file_name + "_from_" + input_language.lower() + type for type in [".cpp",".java",".py"]]

    translate("data/test_corpus/" + input_language.lower() + "/" + source_file, input_language, file_name)
    evaluate_translations(ground_truth_files, translation_files, True)

    rule_set.save_rules() # since user may add/extend rules
