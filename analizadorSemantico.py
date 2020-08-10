import operator as op
import traceback


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
        while op is not None and op.valor != ';':
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
        if nombre == 'imprime':
            raise Error('El nombre de variable {} esta reservado'.format(nombre))
            
        else:
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
            return resultado
    def visitar(self, nodo):
        return getattr(self, nodo.nombre.lower(), self.saltar)(iter(nodo.items))
