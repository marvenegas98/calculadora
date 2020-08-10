import re
from collections import namedtuple



Nodo = namedtuple('Nodo', ('nombre', 'items'))

class AnalizadorSintactico(object):
    def __init__(self, tokens, gramatica):
        self.analizadorLexico = tokens
        self.gramatica = gramatica
        
        self.cont = 0

    def avanzar(self):
        self.token_actual = next(self.generador_tokens, None)
        if self.token_actual is not None:
            self.cont += 1

    def error(self):
        if self.token_actual.valor is not None:
            mensaje = 'Etapa: Análisis Sintáctico: No se esperaba token {}'.format(self.token_actual.valor)
        else:
            mensaje = 'Etapa: Análisis Sintáctico: No se esperaba EOF'
        self.analizadorLexico.error(mensaje)

    def eat(self, nombre_token):
        if self.token_actual is not None and self.token_actual.nombre == nombre_token:
            token = self.token_actual
            self.avanzar()
            return token

    def regla(self, norma):
        
        return Nodo(nombre=norma, items=self.gramatica[norma](self))


    def enlazar(self, norma, texto, ignorar_espacios=True, revisar_eof=True):

        self.generador_tokens = self.analizadorLexico.anlex(texto, ignorar_espacios)
        
        self.token_actual = None
        self.avanzar()
        
        try:
            
            resultado = self.regla(norma)
            if revisar_eof:
                a('EOF')(self)
        except ErrorSintactico:
            self.error()
        else:
            return resultado


class ErrorSintactico(Exception):
    pass


def unir(*args):
    args = (arg if callable(arg) else a(arg) for arg in args)
    return a(*args)


def just(nombre_token):
    def inner(enlazar):
        token = enlazar.eat(nombre_token)
        if token is None:
            raise ErrorSintactico
        return token
    return inner


def comparar(*args):
    def inner(enlazar):
        cnt = enlazar.cont
        try:
            return unir(*args)(enlazar)
        except ErrorSintactico:
            if enlazar.cont != cnt:
                raise ErrorSintactico
    return inner


def saltar(*args):
    def inner(enlazar):
        unir(*args)(enlazar)
    return inner


def cualquiera(*args):
    def inner(enlazar):
        for arg in args:
            resultado = comparar(arg)(enlazar)
            if resultado:
                return resultado
        raise ErrorSintactico
    return inner


def alguno(*args):
    def inner(enlazar):
        resultado = unir(*args)(enlazar)
        while True:
            part = comparar(unir(*args))(enlazar)
            if part:
                resultado.extend(part)
            else:
                break
        return resultado
    return inner


def a(*args):
    def inner(enlazar):
        resultado = []
        for arg in args:
            if arg in enlazar.gramatica:
                arg = enlazar.regla(arg)
            if isinstance(arg, str):
                arg = just(arg)
            if callable(arg):
                arg = arg(enlazar)
            if arg is not None:
                if not isinstance(arg, list):
                    resultado.append(arg)
                else:
                    resultado.extend(arg)
        return resultado
    return inner
    
		
