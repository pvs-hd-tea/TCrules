# Follow-Up Developer Documentation

![overview](./images/overview.png)

## Current state
It was not possible to fully automatize the training/learining procedure, but in the development process we focused on the ability to translate assignments, declarations, for-, while- and if-statements and started with translating entire concepts such as sorting array for example. For a continuation of this project with new members it would be a good start to improve these points.

### Possible future work
1. Fully automate the derivation of the rules, if necessary, so that as little manual work as possible is required.
2. Continue the implementation of the idea of translating entire concepts/algorithms
3. Enlarge the parallel training and test data set

### Where are all necessary functions defined?
* [parser.py](c2c-translator/parser.py) contains the definition of the RuleSet class with all the functions for deriving the rules and translating given line of code or an entire file
* [keywords_lookup.json](c2c-translator/keywords_lookup.json) contains keyword to keyword mappings used for the translation
* [rules.json](c2c-translator/rules.json) contains the derived rules used then for the translation
* [data/parallel_corpus](c2c-translator/data/parallel_corpus) contains the parallel training data set used for deriving the rules
* [concepts.py](c2c-translator/concepts.py) contains the definition of Concepts with functions for checking concepts in code and giving suggestions for improvements of translation
* [concepts.json](c2c-translator/concepts.json) contains the concepts that may match with given code and suggest the more efficient way
* [keywords_concepts.txt](c2c-translator/keywords_concepts.txt) contains the keywords to look up entries in concepts.json

### Add new rules
Of course, rules can also be added manually by modifying the rules.json file. But since this is not what we want, to derive rules for concepts other than assignments, declarations, if-, for- and while-statements, small improvements in parser.py might be necessary, especially for creating correct generalized code. However, you should first try to use the c2c translator without any other implementations.

## Add new concepts
For now, new concepts can only be entered manually and not derived from a training corpus, as this feature is not fully finished and not only does the approach still require validation, it also does not automatically translate. It only gives a suggestion for more efficient translations for certain concepts.

## Results
It was more time consuming and difficult, as we initially thought, to develop a working scheme for deriving rules and translating given line code or source files.

### The initial goal
The goal of this project was to create a rule-based code-to-code translator for the programming languages C++, Java and Python. The main idea was to generate and continuously extend a pattern/rule database using parallel corpora. Then the input source code should be split into parts and translated via the database or by the user.

### Useful collected knowledge
* You do not need a lot of training data, one example per concept is sufficient as long as it is parallel (i.e. available in the three programming languages C++, Java and Python).

## Software Architecture
Below you can take a look at the architecture. 
![architecture](./images/architecture.png)
Here the structure of the DB is presented.
![rules](./images/rules.png)
The training proceeds as follows:
![training](./images/training.png)
The translation proceeds as follows:
![translating](./images/translating.png)
