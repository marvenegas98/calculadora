import traceback
import readline
import operator as op

from analizadorLexico import AnalizadorLexico,Token
from analizadorSintactico import AnalizadorSintactico, a, cualquiera, comparar, alguno
from analizadorSemantico import AnalizadorSemantico,Error






tokens = (
    ('(\d*\.\d+)|(\d+\.\d*)', 'FLOAT'),
    ('\d+', 'ENT'),
    ('\+', 'SUMA'),
    ('-', 'RESTA'),
    ('\*', 'MUL'),
    ('/', 'DIV'),
    ('\)', 'PAR_DER'),
    ('\(', 'PAR_IZQ'),
    ('\w+\s*=', 'ASIG'),
    ('imprime','IMPRIME'),
    ('\w+', 'NOMBRE'),
    ('=', 'EQ'),
    ('\;','PUNTOYCOMA')
    
)

gramatica = {
    
    'FACTOR': cualquiera(
        'FLOAT', 'ENT', 'NOMBRE',
        a(cualquiera('SUMA', 'RESTA'), 'FACTOR'),
        a('PAR_IZQ', 'EXPRESION', 'PAR_DER')),
    'TERMINO': a('FACTOR', comparar(alguno(cualquiera('DIV', 'MUL'), 'FACTOR'))),
    'DEFINIR': a('ASIG', 'EXPRESION'),
    'EXPRESION': a('TERMINO', comparar(alguno(cualquiera('SUMA', 'RESTA'), 'TERMINO'))),
    'PROGRAMA': a(cualquiera('EXPRESION', 'DEFINIR','IMPRIMIR'),'PUNTOYCOMA'),
    'IMPRIMIR': a('IMPRIME', 'NOMBRE')
    
}

analizadorLexico = AnalizadorLexico(tokens)
analizadorSintactico = AnalizadorSintactico(analizadorLexico, gramatica)
analizadorSemantico = AnalizadorSemantico()

def calc_eval(texto):
    ast = analizadorSintactico.enlazar('PROGRAMA', texto)
    #print(ast)
    return analizadorSemantico.visitar(ast)


_bold = '\033[;1m{}\033[0;0m'.format
_red = '\033[1;31m{}\033[0;0m'.format

def run(texto):
    try:          
        rv = calc_eval(texto)
        return rv
        print (rv)
    except (KeyboardInterrupt, EOFError):
        exit(0)
    except SyntaxError as exc:
        msg = traceback.format_exception_only(type(exc), exc)
        #print(''.join(msg[3:] + msg[1:3]), end='')
        return ''.join(msg[3:] + msg[1:3])
    except (ArithmeticError, Error) as exc:
        #print(exc)
        return exc
