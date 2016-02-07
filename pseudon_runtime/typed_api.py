import types

class GenericArg:
    '''
    nth generic arg type
    '''
    def __init__(self, index):
        self.index = index

class Generic:
    def __init__(self, base):
        self.base = base

    def __getitem__(self, *args):
        return GenericInstance(self.base, args)

class GenericInstance:
    def __init__(self, base, args):
        self.base = base
        self.args = args

ElementType = GenericArg(0)
KeyType, ValueType = GenericArg(0), GenericArg(1)

HandlerType = GenericArg(1)

List = Generic(list)
Dictionary = Generic(dict)

Function = Generic(types.FunctionType)

TYPED_API = {
    list: {
        'push':       ([ElementType], None),
        'pop':        ([], ElementType),
        'insert':     ([ElementType], List[ElementType]),
        'length':     ([], int),
        'remove':     ([ElementType], None),
        'remove_at':  ([ElementType, int], None),

        'map':        ([Function[ElementType, HandlerType]], List[HandlerType]),
        'filter':     ([Function[ElementType, bool]], List[ElementType])
    },

    dict: {
        'keys':       ([], List[KeyType]),
        'values':     ([], List[ValueType]),
        'length':     ([], int)
    },

    int: {
        '+':          ([int], int),
        '-':          ([int], int),
        '/':          ([int], int)
    }
}

def ungenerify(message, type, arg_types):
    result = TYPED_API.get(type, {}).get(message)
    if result:
        out_type = []
        for j, arg_type in enumarate(result[0] + [result[1]]):
            if isinstance(arg_type, GenericArg):
                new_type = arg_types[arg_type.index]
            elif isinstance(arg_type, GenericInstance):
                new_type = GenericInstance(
                    arg_type.base,
                    [arg_types[a_type.index]
                     if isinstance(a_type, GenericArg) 
                     else a_type
                     for a_type in arg_type.args])
            else:
                new_type = arg_type
            if j < len(result[0]):
                out_type[0].append(new_type)
            else:
                return out_type, new_type
    else:
        return arg_types, None

