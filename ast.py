from analizadorSintactico import AnalizadorSintactico, a, cualquiera, comparar, alguno, saltar
from util import hacer_imagen

tokens = (
    ('\(', 'PAR_IZQ'),
    ('\)', 'PAR_DER'),
    ('\,', 'SEP'),
    ('\d+', 'NUM'),
    ('"\w+"', 'CADENA')
)
gramatica = {
    'EXPRESION': a(
        saltar('PAR_IZQ'),
        'VALOR', comparar(alguno(saltar('SEP'), 'VALOR')),
        saltar('PAR_DER')
    ),
    'VALOR': cualquiera('CADENA', 'NUM', 'EXPRESION')
}
hilera_analizar = '(1, 2, ("test", ((3), 4)))'

analizadorSintactico = AnalizadorSintactico(tokens, gramatica)
ast = analizadorSintactico.enlazar('EXPRESION', hilera_analizar)

with open('ast.dot', 'w') as f:
    f.write(hacer_imagen(ast))
