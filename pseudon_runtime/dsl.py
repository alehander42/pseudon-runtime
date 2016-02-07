'''
dsl for easier creation of pseudon ast

'''

LITERAL_TYPES = {str: 'string', int: 'int', float: 'float', bool: 'boolean', list: 'list', dict: 'dictionary', None: 'none'}

def to_basic(l):

    if isinstance(l, dict) and 'type' in l:
        return l # Node
    elif isinstance(l, (int, float, bool, set)):
        return {'type': LITERAL_TYPES[type(l)], 'value': l}
    elif l is None:
        return {'type': 'none'}
    elif isinstance(l, list):
        return {'type': 'list', 'elements': list(map(to_basic, l))}
    elif isinstance(l, dict):
        return {'type': 'dict', 'pairs': [(to_basic(k), to_basic(v)) for k, v in l.items()]}
    else:
        return l

def call(callee, args):
    return {'type': 'call', 'callee': Node('call', callee=to_basic(callee), args=list(map(to_basic, args)))}

def local(name):
    return {'type': 'local', 'name': name}

def typename(name):
    return {'type': 'typename', 'name': name}

def to_node(*field_names):
    '''
    returns a helper turning args into to_basic-processed node-type dictionaries

    it could have been done with co_varnames[:co_argcount] but that's cpython-implementation
    dependent
    '''
    def decorator(f):
        def wrapped(*args):
            result = {'type': f.__name__}
            result.update({
                field_name: to_basic(arg) if not isinstance(arg, list) else list(map(to_basic, arg))
            for field_name, arg in zip(field_names, args)})
            return result
        return wrapped
    return decorator

@to_node('test', 'if_true', 'otherwise')
def if_statement(test, if_true, otherwise):
    pass

@to_node('iterable', 'index', 'sequence', 'body')
def for_statement(iterable, index, sequence, body):
    pass

@to_node('name', 'args', 'body')
def function(name, args, body):
    pass

@to_node('local', 'value')
def local_assignment(local, value):
    pass

def to_list(elements):
    '''to_list([2, 4]) => {'type': 'list', ..}'''
    return {'type': 'list', elements: list(map(to_basic, elements))}

def to_dictionary(elements):
    '''to_dictionary(['k', 2, 'v', 4]) => {'type': 'dictionary', ..}'''
    basic = list(map(to_basic, elements))
    return {'type': 'dictionary', pairs: zip(basic[::2], basic[1::2])}





