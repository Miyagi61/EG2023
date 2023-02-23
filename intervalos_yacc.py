# ------------------------------------------------------------
# TPC1 : Intervalos (definição sintática)
#  + [100,200][3,12]
#  + [-4,-2][1,2][3,5][7,10][12,14][15,19]
#  - [19,15][12,6][-1,-3]
#  - [1000,200][30,12]
# ------------------------------------------------------------
import sys
import ply.yacc as yacc
from intervalos_lex import tokens

# The set of syntatic rules
def p_sequencia(p):
    "sequencia : sentido intervalos"
    if p[1] == "+" and p[2][2] < 0 or p[1] == "-" and p[2][2] > 0:
        parser.flag = True
    else:
        print("Num_Intervalos: %d" % p[2][3]['qt'])
        print("Comprimentos: %s" % p[2][3]['len'])
        print("Mais Longo: %d" % p[2][3]['maior'])
        print("Mais Curto: %d" % p[2][3]['menor'])
        print("Amplitude: %d" % abs(p[2][0] - p[2][1]))



def p_sentidoA(p):
    "sentido : '+'"
    p[0] = p[1]

def p_sentidoD(p):
    "sentido : '-'"
    p[0] = p[1]

def p_intervalos_intervalo(p):
    "intervalos : intervalo"
    p[0] = p[1]

def p_intervalos_intervalos(p):
    "intervalos : intervalos intervalo"
    if (p[1][2] < 0 and p[2][2] < 0 and p[1][1] > p[2][0]) or (p[1][2] > 0 and p[2][2] > 0 and p[1][1] < p[2][0]):
        p[0] = p[1]
        p[0][1] = p[2][1]
        p[0][3]['qt'] += 1
        if p[2][2] > p[0][3]['maior']:
            p[0][3]['maior'] = p[2][2]
        if p[2][2] < p[0][3]['menor']:
            p[0][3]['menor'] = p[2][2]
        p[0][3]['len'].append(p[2][2])
    else:
        p[0] = p[2]
        parser.flag = True 

def p_intervalo(p):
    "intervalo : '[' NUM ',' NUM ']'"
    #      (1st , 2nd,dif        ,changed)
    p[0] = [p[2],p[4],p[4] - p[2],
            {'qt':1,
             'len':[p[4] - p[2]],
             'maior':p[4] - p[2],
             'menor':p[4] - p[2]}]

# Syntatic Error handling rule
def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

# Start parsing the input text
for line in sys.stdin:
    parser.success = True
    parser.flag = False
    parser.last = 0
    parser.parse(line)

    if parser.success:
        if parser.flag:
            print('Incorreta sintaticamente')
