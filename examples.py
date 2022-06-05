import ast
from pprint import pprint
import tokenize
from math import sqrt, pow, exp
from matplotlib import pyplot as plt

import pandas as pd
import seaborn as sns
import spacy

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
 


def squared_sum(x):
    """ return 3 rounded square rooted value """
    return round(sqrt(sum([a*a for a in x])),3)

# doesn’t work well with the sparse vectors of text embeddings 
def euclidean_distance(x,y):
    """ return euclidean distance between two lists """
    return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

# euler's const
def distance_to_similarity(distance):
    return 1/exp(distance)

# takes only the set of unique words into account
def jaccard_similarity(x,y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

# not affected by the magnitude/length of the feature vectors
def cos_similarity(x,y):
    """ return cosine similarity between two lists """
    numerator = sum(a*b for a,b in zip(x,y))
    denominator = squared_sum(x)*squared_sum(y)
    return round(numerator/float(denominator),3)


sentences = ["The bottle is empty", "There is nothing in the bottle"]
sentences = [sent.lower().split(" ") for sent in sentences]
jaccard_similarity(sentences[0], sentences[1]) # 0.43

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")
embeddings = [nlp(sentence).vector for sentence in sentences]
distance = euclidean_distance(embeddings[0], embeddings[1])
print(distance) # 1.86
distance_to_similarity(distance) # 0.85
cos_similarity(embeddings[0], embeddings[1]) # 0.89

#######################################################################

headlines = [
#Crypto
'Investors unfazed by correction as crypto funds see $154 million inflows',
'Bitcoin, Ethereum prices continue descent, but crypto funds see inflows',
 
#Inflation
'The surge in euro area inflation during the pandemic: transitory but with upside risks',
"Inflation: why it's temporary and raising interest rates will do more harm than good",
 
#common
'Will Cryptocurrency Protect Against Inflation?']

labels = [headline[:20] for headline in headlines]

def create_heatmap(similarity, cmap = "YlGnBu"):
    df = pd.DataFrame(similarity)
    df.columns = labels
    df.index = labels
    fig, ax = plt.subplots(figsize=(5,5))
    sns.heatmap(df, cmap=cmap)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(headlines)
arr = X.toarray()

create_heatmap(cosine_similarity(arr))


docs = [nlp(headline) for headline in headlines]
similarity = []
for i in range(len(docs)):
    row = []
    for j in range(len(docs)):
      row.append(docs[i].similarity(docs[j]))
    similarity.append(row)

create_heatmap(similarity)



#######################################################################

def main():
    with open("examples.py", "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)


class NodeVisitor(ast.NodeVisitor):
    def visit_Str(self, tree_node):
        print('{}'.format(tree_node.s))


class NodeTransformer(ast.NodeTransformer):
    def visit_Str(self, tree_node):
        return ast.Str('String: ' + tree_node.s)

tree_node = ast.parse('''
fruits = ['grapes', 'mango']
name = 'peter'

for fruit in fruits:
    print('{} likes {}'.format(name, fruit))
''')

NodeTransformer().visit(tree_node)
NodeVisitor().visit(tree_node)

tree_node = ast.fix_missing_locations(tree_node)
exec(compile(tree_node, '', 'exec'))


expression = '6 + 8'
code = ast.parse(expression, mode='eval')

print(eval(compile(code, '', mode='eval')))
print(ast.dump(code))

with open('hello.py', 'rb') as f:
    for token in tokenize.tokenize(f.readline):
        print(token.type, token.string, token.start, token.end)

        
if __name__ == "__main__":
    main()
