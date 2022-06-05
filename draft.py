import ast
from io import BytesIO, StringIO
import os
import parser
import pprint
import tokenize
import token
import keyword # python keywords or soft keywords, eg. False, None, and, break, def, if, import return etc.


"""st = parser.suite(open('hello.py').read())
tup = st.totuple()
pprint.pprint(tup)
"""

"""with open("hello.py", "r") as source:
    tree = ast.parse(source.read()) 
print(ast.dump(tree))"""

def print_tokens(s):
    for tok in tokenize.tokenize(BytesIO(s.encode('utf-8')).readline):
        print(tok)

with tokenize.open('hello.py') as f:
    tokens = tokenize.generate_tokens(f.readline)
    #tokens = tokenize.tokenize(f.readline)
    token_list = [t for t in tokens]

    """for t in tokens:
        print(t.string, t.start, t.end, token.tok_name[t.type])"""
    
    print([t.string for t in token_list if t.type=="NUMBER"])

    print_tokens('x + 1\n')
    print_tokens('a or α\n')
    print_tokens('012\n') # 0 12 \n
    print_tokens('0x1.0 # COMMENT\n') # 0x1 .0 \n
    print_tokens('1.0000000000000001\n') # advantage over ast module
    print_tokens('"this is" " fun"\n')

    """OP, STRING, NUMBER, NEWLINE, ENDMARKER, NL, NAME, ERRORTOKEN, COMMENT"""
    
    ast.dump(ast.parse('1.0000000000000001'))

    print([f"or is keyword" if keyword.iskeyword('or') else f"or is not keyword"])