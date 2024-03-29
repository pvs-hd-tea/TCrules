# TCrules

The goal of this project is to create a rule-based code-to-code translator for the programming languages C++, Java and Python. The main idea is to generate and continuously extend a pattern/rule database using parallel corpora. Then the input source code is split into parts and translated via the database or by the user.

> Begginer Software Practical "AI Methods and Tools for Programming", Summer 2022

> Authors: Vivian Kazakova, Jonas Ochs

## Pipeline
### Training
For training the model, i.e. deriving the rules, we use a parallel corpus we created ourself which consists of 8 files per language, which cover the main concepts the model could translate (assignments, declarations, if-, while- and for-statements).
The model goes through the files line by line. For each line, the s-expression and the parse tree is created using the [tree-sitter](https://github.com/tree-sitter/tree-sitter) parsers. 
Then the keyword from the first child of the root node is extracted. If this is a statement (if-, while- or for-statement) and there is not a rule derived for it yet, the block is determined, the generic expression for it is created and the rule is added to the database.
For example, we get the following generic expressions and rule for any if-statement:
```
['if (@) {\n    @\n}\n', 'if (@) {\n    @\n}\n', 'if @:\n    @\n']
```
where `@` is used as a placeholder and the expressions correspond to the C++, JAVA and PYTHON languages.
```json
"if_statement": [
	[
		"if (@) {\n    @\n}\n",
		"if (@) {\n    @\n}\n",
		"if @:\n    @\n"
	]
],
```
Otherwise, we either add a new rule or extend an existing rule for a particular line of code. The generic expression for it is created again and the database is updated.
For example, we obtain the rule "local_variable_declaration" with the following list of generic expressions for any variable declaration:
```
['type name = value;\n', 'type name = value;\n', 'name = value\n']
```
And later the rule is extended, for instance, by:
```
['type name = name operator value;\n', 'type name = name operator value;\n', 'name = name operator value\n']
```
Since the parsing trees and keywords in Python sometimes differ from those in C++ and Java, an additional check is performed, and if this is the case, the corresponding rule is also created or extended.

Finally, the derived rules and the keywords are stored in the rules.json and keywords_treesitter.txt files respectively. 

### Usage
After the database is created, the model might start translating single line of code or an entire file. 

1. Translating a line:

Given a line of code as an input, we create the s-expression and the parse tree and determine the keyword. Based on the keyword, we search for the corresponding rule. Then the generic expression of the input is created and we look for the best match between the input and the rules. If one is found, these generic expressions would be transformed. For this, the input code is used so that we obtain e.g. the variable name or specific keywords such as "bool" etc.
For example:
```
Input code: a = 5.5
Input language: PYTHON

S-expression: (module (expression_statement (assignment left: (identifier) right: (float))))
Parse tree: <tree_sitter.Tree object at 0x7fc343530250>
Keyword: expression_statement

Match with existing rule: ('expression_statement', 100) 
Generic expression: name = value

Match with entry within the rule: ('name = value\n', 100, 0)

Entry 1 before transformation: type name = value;
Entry 1 after: float a = 5.5;

Entry 2 before: type name = value;
Entry 2 after: float a = 5.5;

Entry 3 before: name = value
Entry 3 after: a = 5.5

Output:	CPP: float a = 5.5;
		JAVA: float a = 5.5;
		PYTHON: a = 5.5
```

2. Translating a file:

The translation of an entire file given as an input proceeds similar, but the main point here is that the file is split into its main parts/blocks. The source file is read line by line and the single blocks (line of code or statement such as if-, while- or for-statements) are translated separately and then joined again into a complete file.

## Repository structure

Our repository is called c2c-translator and has the following structure:
```
c2c-translator
	data
		data/big_eval_corpus
		data/evaluation
			metrics.txt
			wrong.txt
		data/geeks_for_geeks_dataset
		data/generate_test_dataset
		data/parallel_corpus
		data/test_corpus
		data/translations
	concepts.json
	concepts.py
	example.py
	keywords_concepts.txt
	keywords_lookup.json
	keywords_treesitter.txt
	parser.py
	rules.json
	suggestion.txt
	test.py
	train.py
	images
ACCOUNTING.md
DOCUMENTATION.md
FOLLOW-UP.md
README.md
LICENSE	
```
In the table below the main files and their description can be found:

| File | Description |
| ---  | ---         |
|[parser.py](c2c-translator/parser.py) | The main script containing the RuleSet class with the functions for generating the rules and translating a given input (single code line or a whole file) |
|[example.py](c2c-translator/example.py) | Usage example |
|[rules.json](c2c-translator/rules.json) | Pattern/rule database |
|[keywords_treesitter.txt](c2c-translator/keywords_treesitter.txt) | List with root node first children keyword from tree-sitter |
|[keywords_lookup.json](c2c-translator/keywords_lookup.json) | keyword to keyword mappings |
|[train.py](c2c-translator/train.py) | Script for deriving the rules using the parallel corpus |
|[test.py](c2c-translator/test.py) | Evaluation script on files from the test_corpus, calculates metrics, stores translations and wrong translated lines |
|[concepts.py](c2c-translator/concepts.py) | Script containing the Concepts class with functions for matching known concepts saved in concepts.json |
|[keywords_concepts.txt](c2c-translator/keywords_concepts.txt) | Containing entries of the concept database |
|[suggestion.txt](c2c-translator/suggestion.txt) | Containing the suggestion made by the concept script for translating more efficiently |
|[concepts.json](c2c-translator/concepts.json) | File containing concepts |
|[data/parallel_corpus](c2c-translator/data/parallel_corpus)| Folder containing the parallel corpus for generating the rules |
|[data/test_corpus](c2c-translator/data/test_corpus)| Folder containing the test corpus for evaluating the translations |
|[data/big_eval_corpus](c2c-translator/data/big_eval_corpus)| Folder containing an evaluation dataset | 
|[data/translation](c2c-translator/data/translations)| Folder containing the translations |
|[data/evaluation](c2c-translator/data/evaluation)| Folder containing a file with the metrics from the evaluation and a file with the wrong translations |
|[data/generate_test_dataset](c2c-translator/data/generate_test_dataset)| Folder containing scripts for generating the big test datasets (assignment, declaration, if and while statements) |
|[data/geeks_for_geeks](c2c-translator/data/geeks_for_geeks)| Folder containing the parallel corpus from Geeks for Geeks |


## Evaluation
### Data
The following datasets are used for evaluating the model.
|Dataset | #Examples| Comment|
|----------------|----------------|----------------
| [test_corpus](c2c-translator/data/test_corpus) | 10 files per language | parallel dataset used in the test.py script for testing and evaluating the translations |
| [big_eval_corpus](c2c-translator/data/big_eval_corpus) | 4 files per language | bigger dataset used for evaluating precision (in the test.py script) |

### Script
The test.py script, which uses the parallel test corpus, calculates the precision score and stores the metrics in the data/evaluation/metrics.txt file. The translations are stored in the translations folder and the incorrect translations are stored in the data/evaluation/wrong.txt file. 
The script requires a file and an input language. Then it translates the file, compares it with the ground truth and counts the correct translations so that in the end the precision score is calculated.


## Challenges
The most difficult thing was to start from scratch. We found it discouraging that our first ideas and approaches were rejected. That's why we were also under time pressure.

There was a lot of research before we started the actual implementation. We decided to use tree-sitter so that we could compare the inputs in the three programming languages. However, the syntax and the keywords are not universal and each language has its differences, which of course makes it difficult to cover all of them.

Working in a team could be also mentioned here. Since each of us has their own ideas and programming style, it was not always easy to come to a compromise. 

## Future work
It is an interesting project that requires creativity and persistence, and in which a lot of work could be invested.

At the moment, the biggest drawback is that for deriving new rules, the code in the parser.py file might need to be extended manually.

Future work on this project may include the following tasks. The derivation of rules could be automated, if necessary, so that as little manual work as possible is required. The idea of translating entire concepts/algorithms should be completed. The parallel training dataset needs to be enlarged so that more concepts can be translated.

## Conclusion
We have successfully created the procedure for deriving the rules using the parallel corpus and implemented the translation of individual lines of code and entire files. A parallel test dataset and a pipeline for it have been created, as well as an evaluation data set and an evaluation script.

Nevertheless, there are still some limitations and areas of investment.
