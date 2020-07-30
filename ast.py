from parser import Parser, a, anyof, someof, maybe, skip
from util import to_dot

tokens = (
    ('\(', 'L_PAR'),
    ('\)', 'R_PAR'),
    ('\,', 'SEP'),
    ('\d+', 'NUM'),
    ('"\w+"', 'STR')
)
grammar = {
    'EXPR': a(
        skip('L_PAR'),
        'VALUE', maybe(someof(skip('SEP'), 'VALUE')),
        skip('R_PAR')
    ),
    'VALUE': anyof('STR', 'NUM', 'EXPR')
}
string_to_parse = '(1, 2, ("test", ((3), 4)))'

parser = Parser(tokens, grammar)
ast = parser.parse('EXPR', string_to_parse)

with open('ast.dot', 'w') as f:
    f.write(to_dot(ast))
