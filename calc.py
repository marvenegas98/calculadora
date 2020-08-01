import traceback
import readline
import operator as op

from analizadorSintactico import AnalizadorSintactico, a, cualquiera, comparar, alguno


class Error(Exception):
    pass

class AnalizadorSemantico(object):

    def __init__(self):
        self.ops_un = {
            '-': op.neg,
            '+': op.pos
        }
        self.ops_bin = {
            '*': op.mul,
            '/': op.truediv,
            '+': op.add,
            '-': op.sub
        }
        self.vars = {}

    def expresion(self, items):
        resultado = self.visitar(next(items))
        op = next(items, None)
        while op is not None:
            resultado = self.ops_bin[op.valor](resultado, self.visitar(next(items)))
            op = next(items, None)
        return resultado

    def termino(self, items):
        return self.expresion(items)

    def factor(self, items):
        item = next(items)
        if item.nombre == 'PAR_IZQ':
            resultado = self.visitar(next(items))
        elif item.nombre in ('SUMA', 'RESTA'):
            resultado = self.ops_un[item.valor](self.visitar(next(items)))
        elif item.nombre == 'NOMBRE':
            if item.valor not in self.vars:
                raise Error(
                    'Variable {} no esta definida'.format(item.valor))
            resultado = self.vars[item.valor]
        else:
            resultado = int(item.valor)
        next(items, None)
        return resultado

    def definir(self, items):
        nombre = next(items).valor.split('=')[0].rstrip()
        self.vars[nombre] = self.visitar(next(items))
   
    def saltar(self, items):
        return self.visitar(next(items))
    def imprimir(self, items):
        item = next(items)
        if item.nombre == 'IMPRIME':
            item = next(items)
        if item.nombre == 'NOMBRE':
            if item.valor not in self.vars:
                raise Error(
                    'Variable {} no esta definida'.format(item.valor))
            resultado = self.vars[item.valor]
            print(resultado)
    def visitar(self, nodo):
        return getattr(self, nodo.nombre.lower(), self.saltar)(iter(nodo.items))


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
    ('=', 'EQ')
    
)

gramatica = {
    
    'FACTOR': cualquiera(
        'FLOAT', 'ENT', 'NOMBRE',
        a(cualquiera('SUMA', 'RESTA'), 'FACTOR'),
        a('PAR_IZQ', 'EXPRESION', 'PAR_DER')),
    'TERMINO': a('FACTOR', comparar(alguno(cualquiera('DIV', 'MUL'), 'FACTOR'))),
    'DEFINIR': a('ASIG', 'EXPRESION'),
    'EXPRESION': a('TERMINO', comparar(alguno(cualquiera('SUMA', 'RESTA'), 'TERMINO'))),
    'PROGRAMA': cualquiera('EXPRESION', 'DEFINIR','IMPRIMIR'),
    'IMPRIMIR': a('IMPRIME', 'NOMBRE')
    
}

analizadorSintactico = AnalizadorSintactico(tokens, gramatica)
analizadorSemantico = AnalizadorSemantico()

def calc_eval(texto):
    ast = analizadorSintactico.enlazar('PROGRAMA', texto)
    print(ast)
    return analizadorSemantico.visitar(ast)


_bold = '\033[;1m{}\033[0;0m'.format
_red = '\033[1;31m{}\033[0;0m'.format

if __name__ == '__main__':
    while True:
        try:
            texto = input(_bold('> '))
            if not texto:
                continue
            rv = calc_eval(texto)
            
            if rv is not None:
                print(' ', _bold(rv))
        except (KeyboardInterrupt, EOFError):
            exit(0)
        except SyntaxError as exc:
            msg = traceback.format_exception_only(type(exc), exc)
            print(_red(''.join(msg[3:] + msg[1:3])), end='')
        except (ArithmeticError, Error) as exc:
            print(_red(exc))
