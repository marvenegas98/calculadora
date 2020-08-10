import re
from collections import namedtuple

Token = namedtuple('Token', ('nombre', 'valor'))


class AnalizadorLexico(object):
    """
     Toma una hilera y produce una secuencia de instancias de Token. Si no encuentra coincidencia,
     se levanta un error de sintaxis
    """
    def __init__(self, patrones):
        """
        :param patrones: Secuencia de tuplas con patron expresion regular y nombre de token
         patrones dependen del orden, el primero en hacer coincidencia gana
        """
        self.patrones = [
            (re.compile(bytes(p, 'utf8')), nombre) for p, nombre in patrones]
        

    def anlex(self, hilera, ignorar_espacios=True):
        """
        :param hilera: hilera de entrada
        :param ignorar_espacios: si es True, todos los espacios en blanco se saltan
        Se devuelve un generador de tokens
        """
        self.hilera = bytearray(hilera, 'utf8')
        self.pos = 0
        posfinal = len(self.hilera)

        while self.pos != posfinal:
            if ignorar_espacios and self.hilera[self.pos: self.pos + 1].isspace():
                self.pos += 1
                continue
            for p, nombre in self.patrones:
                m = p.match(self.hilera[self.pos:])
                if m is not None:
                    val, sobrante = m.group(), m.end()
                    yield Token(nombre, str(val, 'utf8'))
                    self.pos += sobrante
                    break
            else:
                self.error('Etapa: Análisis Lexico: Caracter Ilegal')
        yield Token('EOF', None)

    def error(self, mensaje):
        raise SyntaxError(mensaje, self.info_error())

    def info_error(self, f_nombre=None):
        pos = self.pos + 1
        hilera = self.hilera
        num_linea = hilera[:pos].count(b'\n')
        ini_linea = max(hilera.rfind(b'\n'), 0)
        fin_linea = max(hilera.find(b'\n'), len(hilera))
        linea = str(hilera[ini_linea:fin_linea], 'utf-8')
        sobrante = pos - ini_linea
        return (f_nombre, num_linea, sobrante, linea)
