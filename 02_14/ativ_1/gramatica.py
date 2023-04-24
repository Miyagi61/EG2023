from lark import Lark
from lark import Transformer


gramatica = open("gic.txt", "r").read() 

class Gramatica(Transformer):
    pass


p = Lark(gramatica, start="programa") 

tree = p.parse(open("testes.txt", "r").read())

data = Transformer().transform(tree) # chamar o transformer para obter