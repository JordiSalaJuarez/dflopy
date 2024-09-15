import ast

class GenFlow(ast.NodeVisitor):
    def __init__(self, module, tree):
        self.module = module
        self.caller = [module]
        self.flow = []
        self.visit(tree)

    def visit_ImportFrom(self, node):
        match node:
            case ast.ImportFrom(module, [ast.alias(name)]):
                self.flow.append(f'extern("{module}", "{name}", "{self.module}").')
        self.generic_visit(node)

    def visit_Call(self, node):
        caller = self.caller[-1]
        match node.func:
            case ast.Name(callee):
                self.flow.append(f'calls("{caller}","{callee}","{self.module}").')
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.flow.append(f'function("{node.name}","{self.module}").') 
        self.caller.append(node.name)
        self.generic_visit(node)
        self.caller.pop()

src_A = '''
from B import foo

def main():
    foo(a)
'''
src_B = '''
from C import bar
from D import baz
def foo():
    bar()
    baz()
'''
src_C = '''
from D import baz
def bar():
    baz()
'''
src_D = '''
def baz():
    pass
'''
modules = ["A", "B", "C", "D"]
srcs = [src_A, src_B, src_C, src_D]
trees = [ast.parse(src) for src in srcs]
flows = [GenFlow(module, tree) for module, tree in zip(modules, trees)]

src_dl = '''
.decl function(name:symbol, context:symbol)
.decl calls(caller:symbol,callee:symbol,context:symbol)
.decl extern(module: symbol, name: symbol, context:symbol)
.decl callGraph(src: symbol, sink: symbol)
.output callGraph

callGraph(x,y) :- calls(x,y,ctx), function(y, ctx).
callGraph(x,y) :- calls(x,y,ctx1), extern(ctx2,y,ctx1), function(y,ctx2).
callGraph(x,z) :- callGraph(x,y), callGraph(y,z).

''' + '\n\n'.join('\n'.join(flow.flow) for flow in flows)

print(src_dl)
















