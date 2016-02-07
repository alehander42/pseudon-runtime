import functools

def remove_at(receiver, index): # because lambdas cant have statements fucking genius, guido
    del receiver[index]

API = {
    list: {
        'push':       list.append,
        'pop':        list.pop,
        'length':     len,
        'insert':     list.insert,
        'remove_at':  remove_at,
        'remove':     list.remove,

        'map':        map,
        'filter':     filter,
        'reduce':     functools.reduce
    },

    dict: {
        'length':     len,
        'keys':       dict.keys,
        'values':     dict.values
    },

    int:  {
        '+':          int.__add__,
        '-':          int.__sub__,
        '/':          int.__divmod__
    }
}

def translate(cell, message):
    result = API.get(type(cell), {}).get(message)
    return result or message
