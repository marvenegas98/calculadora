import uuid
from analizadorSintactico import Token, Nodo


def hacer_imagen(ast):
    resultado = [
        'strict digraph "AST" {',
        'size="16,14"; ratio = fill;'
    ]
    _escape = lambda s: s.replace('"', r'\"')
    
    def format_node(node, uid):
        if isinstance(node, Token):
            label = '{} [{}]'.format(*map(_escape, (node.nombre, node.valor)))
        elif isinstance(node, Nodo):
            label = '{}'.format(*map(_escape, (node.nombre,)))
        else:
            raise ValueError("Can't format node {}".format(node))
        return '"{}" [label="{}"];'.format(uid, label)

    def walk(node, uid):
        resultado.append(format_node(node, uid))
        if isinstance(node, Nodo):
            for i in node.items:
                child_uid = uuid.uuid4().hex
                walk(i, child_uid)
                resultado.append('"{}" -> "{}";'.format(uid, child_uid))

    uid = uuid.uuid4().hex
    walk(ast, uid)
    resultado.append('}')
    return '\n'.join(resultado)
