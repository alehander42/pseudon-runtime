from pseudon_runtime import api_translator

def compile(ast):
    '''
    compiles the ast into a callable AstFunction
    '''
    return AstFunction(ast)


class AstFunction:

    def __init__(self, ast):
        self.ast = ast

    def __call__(self, *args):
        return AstEvaluator(self.ast, args).evaluate(globals())

class AstEvaluator:

    def __init__(self, ast, args):
        self.ast = ast
        self.args = args

    def evaluate(self, env):
        self.env = env
        self.env.update({
            arg_name: arg 
            for arg_name, arg in zip(self.ast['args'], self.args)
        })
        return self._evaluate_block(self.ast['body'])

    def _evaluate_block(self, block):
        for j, sexp in enumerate(block):
            result = self._evaluate_node(sexp)
            if j == len(block) - 1:
                return result

    def _evaluate_node(self, node):
        if node['type'] == 'call':
            return self._evaluate_node(node['callee'])(*map(self._evaluate_node, node['args']))
        elif node['type'] == 'method_call':
            a = self._evaluate_node(node['receiver'])
            message = api_translator.translate(a, node['message'])
            if isinstance(method_call, str): # node
                return getattr(a, message)(*map(self._evaluate_node, node['args']))
            else:
                return method_call(*map(self._evaluate_node, node['args']))                
        elif node['type'] == 'local':
            return self.env[node['name']]
        elif node['type'] == 'local_assignment':
            self.env[node['local']] = self._evaluate_node(node['value'])
        elif node['type'] in ['int', 'float', 'boolean']:
            return node['value']
        elif node['type'] == 'none':
            return None
        elif node['type'] == 'if_statement':
            result = self._evaluate_node(node['test'])
            if result:
                self._evaluate_node(node['if_true'])
            else:
                self._evaluate_node(node['otherwise'])


