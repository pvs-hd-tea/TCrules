# TCrules
The goal of this project is to create a rule-based code-to-code translator for the programming languages Python, Java and C++. The main idea is to generate and continuously extend a pattern/rule database using parallel corpora. Then the input source code is split into parts and translated via the database or by humans. See [DOCUMENTATION.md](DOCUMENTATION.md) and [FOLLOW-UP.md](FOLLOW-UP.md) for more details.

> Begginer Software Practical "AI Methods and Tools for Programming", Summer 2022
>
> Authors: Vivian Kazakova, Jonas Ochs

## Getting Started

### Prerequisites
Make sure you have Python 3.8 and tree_sitter installed. See [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter) for more details on installing the module.

### Usage
Create a `RuleSet` and generate the rule database:
```python
import parser

rule_set = parser.RuleSet()

rule_set.derive_rules(parser.files)
rule_set.save_rules()
```
Create a `RuleSet` and translate a given source file:
```python
import parser

rule_set = parser.RuleSet()
translations = rule_set.translate_file(source_file, input_language)
for line in translations:
	print(line)
```
Create a `RuleSet` and translate a given code line:
```python
import parser

if __name__ == "__main__":

    rule_set = parser.RuleSet()
    input_code = "a = 5.5"
    input_language = parser.PYTHON
    languages = [parser.CPP, parser.JAVA, parser.PYTHON]

    print(f"\nInput code: {input_code}\nInput language: {input_language}\nTranslating...")

    translations,_ = rule_set.translate_line(input_code, input_language)
    for i, translation in enumerate(translations):
        print(f"{languages[i]}: {translation}")
```
See the example in [example.py](example.py) as well. Run
```
python3 example.py
```

## Overview
### Files
| File | Description |
| ---  | ---         |
|[parser.py](parser.py) | The main script containing the RuleSet class with the functions for generating the rules and translating a given input |
|[concepts.py](concepts.py) | Class for creating and saving reusable concepts from all three languages e.g. sorting, searching for a certain element, etc., that don't need to be translated line by line but rather just matching optimized versions of said concepts. |
|[rules.json](rules.json) | Pattern/rule database |
|[keywords_treesitter.txt](keywords_treesitter.txt) | List with root node first children keyword from tree-sitter |
|[keywords_lookup.json](keywords_lookup.json) | keyword to keyword mappings |
|[example.py](example.py) | Usage example |
|[train.py](train.py) | Script for deriving the rules using the parallel corpus |
|[test.py](test.py) | Evaluation script on files from the test_corpus, calculates metrics, stores translations and wrong translated lines |
|[data/parallel_corpus](data/parallel_corpus)| Folder containing the parallel corpus for generating the rules |
|[data/test_corpus](data/test_corpus)| Folder containing the test corpus for evaluating the translations |
|[data/translation](data/translations)| Folder containing the translations |
|[data/evaluation](data/evaluation)| Folder containing a file with the metrics from the evaluation and a file with the wrong translations |
|[data/generate_test_dataset](data/generate_test_dataset)| Folder containing scripts for generating the big test datasets (assignment, declaration, if and while statements) |
|[data/geeks_for_geeks](data/geeks_for_geeks)| Folder containing the parallel corpus from Geeks for Geeks |

### Data
The following datasets are used for evaluating the model.
|Dataset | #Examples| Comment|
|----------------|----------------|----------------
| [test_corpus](data/test_corpus) | 10 files per language | parallel dataset used for testing (in the test.py script) |
| [evaluation_corpus](data/evaluation_corpus) | 4 big files per language | dataset used for evaluation (in the big_eval.py script) |


#### Evaluation

The test.py script which uses the parallel test corpus, calculates the precision score and stores the results in the `data/evaluation/metrics.txt` file. The translations are stored in the `translations` folder and the wrong translations in the `data/evaluation/wrong.txt` file.

Run
```
python3 test.py [-h] -f FILE -l {cpp,java,python} [-e {True,False}]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  input source code to be translated
  -l {cpp,java,python}, --language {cpp,java,python}
                        input language to be translated from
  -e {True,False}, --evaluation {True,False}
                        store evaluation metrics in a separate file
```
For example:
```
python3 test.py -f simple.java -l java
```

#### Rules
There are 6 rules for translating code lines and statements between the three programming languages C++, Java and Python defined in the rules.json file. Existing rules can be changed and new ones can be added by enlarging the parallel corpus and running the database generation script. The name of the rule corresponds to the keyword extracted from the tree-sitter parse tree and each rule consists of one or multiple lists of generic expressions for the three languages.
Example:
```json
"expression_statement": [
    [
        "type name = value;\n",
        "type name = value;\n",
        "name = value\n"
    ],
    [
        "std::cout<<@;\n",
        "System.out.println(@);\n",
        "print(@)\n"
    ]
],
"if_statement": [
    [
        "if (@) {\n    @\n}\n",
        "if (@) {\n    @\n}\n",
        "if @:\n    @\n"
    ]
]
```

#### Concepts
Concepts are mostly compromised of the most efficient ways of translating reocurring concepts into different programming languages. Every language has its own way of dealing with sorting of arrays or has its own style of for example constructor definitions, finding the highest value in an array, etc.. Translating those concepts without using the advantages of every language would technically be possible, but rather inefficient. 
Therefore input code is checked on concepts and if a reocurring principle is found, the language specific golden way is chosen.
Example:
```json
{
    "sortarr_py": [
        [
            "arr = [4,3,2,1]\narr.sort()"
        ]
    ],
    "sortarr_cpp": [
        [
            "#include <algorithm>\n#include <vector>\nstd::vector<int> arr {4,3,2,1};\nstd::sort(arr.begin(),arr.end());"
        ]
    ],
    "sortarr_jv": [
        [
            "import java.util.Arrays;\nint[] arr = {4,3,2,1};\nArrays.sort(arr);"
        ]
    ]
}
```
