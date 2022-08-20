import os
import textwrap
import re
import json
from tree_sitter import Language, Parser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    # Jonas
    [
    '/Users/jonas/Documents/GitHub/tree-sitter-cpp',
    '/Users/jonas/Documents/GitHub/tree-sitter-java',
    '/Users/jonas/Documents/GitHub/tree-sitter-python'
    ]
    # Vivian
    # [
    #     '/home/vivi/src/tree-sitter-python',
    #     '/home/vivi/src/tree-sitter-java',
    #     '/home/vivi/src/tree-sitter-cpp'
    # ]
)

PY_LANGUAGE = Language('build/my-languages.so', 'python')
JV_LANGUAGE = Language('build/my-languages.so', 'java')
CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

PYTHON = "PYTHON"
JAVA = "JAVA"
CPP = "CPP"


class Concept:
    def __init__(self):
        if not os.path.isfile("concepts.json"):
            self.concepts = {}
        else:
            with open("concepts.json", encoding="utf8") as file:
                self.concepts = json.load(file)
                print(f"Loading {len(self.concepts)} concepts ... Done ...")


    def save_rules(self):
        """store derived rules in json format"""
        with open("concepts.json", "a+", encoding="utf8") as file:
            file.truncate(0)
            file.seek(0)
            json.dump(self.concepts, file, indent=4)

    def match_concept(self, input_code):










