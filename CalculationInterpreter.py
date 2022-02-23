class Empty(Exception):
    ''' Nova excecao - sub classe de Exception'''
    pass

class Invalid(Exception):
    ''' Nova excecao - sub classe de Exception'''
    pass

class InvalidExpression(Exception):
    ''' Nova excecao - sub classe de Exception'''
    pass

class IncoerenciaParenteses(Exception):
    ''' Nova excecao - sub classe de Exception'''
    pass

import sys, traceback

class PilhaLista:
    '''Pilha como uma lista.'''
    
    # Construtor da classe PilhaLista
    def __init__(self):
        self._pilha = [] # lista que contera a pilha
        
    # retorna o tamanho da pilha
    def __len__ (self):
        return len(self._pilha)
    
    # retorna True se pilha vazia
    def is_empty(self):
        return len(self._pilha) == 0
    
    # empilha novo elemento e
    def push(self, e):
        self._pilha.append(e)
        
    # retorna o elemento do topo da pilha sem retira-lo
    # excecao se pilha vazia
    def top(self):
        if self.is_empty( ):
            raise Empty("Pilha vazia")
        return self._pilha[-1]
    
    # desempilha elemento
    # excecao se pilha vazia
    def pop(self):
        if self.is_empty( ):
            raise Empty("Pilha vazia")
        return self._pilha.pop( )
        

# Código:

listavar = []
listaval = []

# verifica se os parenteses estao balanceados
def Verifica_parentesis(expressao):
    contador = 0
    exp = str(expressao)
    for i in exp:
        if i == "(": 
            contador +=1
        elif i == ")":
            contador -= 1
            if contador < 0: return False
    if contador != 0: return False
    return True
        
# lista de prioridade
def prioridade(x):
    if x == '=': return 0 # e o de menor?
    elif x == '+': return 1
    elif x == '-': return 1
    elif x == '*': return 2
    elif x == '/': return 2
    elif x == '#': return 3
    elif x == '_': return 3
    elif x == '^': return 4
    elif x == '(': return 5
    elif x == ')': return 6
    else: return None # nao e operador
    
# recebe a expressao (string) com espacos e a "arruma"
def arruma(exp):
    novo = []
    # separa os elementos
    exp = exp.replace("**","^")
    k = 0
    while k < len(exp):
        if exp[k] == " ": 
            k += 1
            continue
        elem = ""
        # se nao e operador:
        if prioridade(exp[k]) == None:
            ind = True
            while prioridade(exp[k]) == None and exp[k] != " " and ind:
                elem += exp[k]
                if k < len(exp) - 1:
                    k += 1
                else:
                    ind = False
        # se e operador
        elif prioridade(exp[k]) != None:
            elem = exp[k]
            ind = False
        if elem != "":
            novo.append(elem)
        if ind != True:
            k += 1
    return novo

# recebe lista
# troca o +,- por #,_ se forem unarios
# retorna lista
def arruma_unarios(exp):
    novo = exp
    for k in range(len(exp)):
        if k == 0 and prioridade(exp[k]) == 1:
            if exp[k] == "+":
                novo[k] = "#"
            if exp[k] == "-":
                novo[k] = "_"
        if k != 0 and prioridade(exp[k]) == 1:
            if prioridade(exp[k-1]) != None:
                if exp[k] == "+":
                    novo[k] = "#"
                if exp[k] == "-":
                    novo[k] = "_"
    return novo

# recebe uma lista
# traduz para pos-fixa
# retorna lista ou False caso de errado
def TraduzPosFixa(exp): 
    pope = PilhaLista() # pilha de operadores
    exppf = []
    a = 0
    b = len(exp)
    for k in exp:
        # se k e ( 
        if prioridade(k) == 5:
            a += 1
            pope.push(k)
        # se k e )
        elif prioridade(k) == 6:
            a += 1
            while prioridade(pope.top()) != 5:
                exppf.append(pope.pop())
            pope.pop()
        # se k e operador != de ( ou ):
        elif prioridade(k) != None:
            if pope.is_empty(): pope.push(k)
            elif prioridade(k) > prioridade(pope.top()):
                pope.push(k)
            elif prioridade(k) <= prioridade(pope.top()):
                while (not pope.is_empty()) and prioridade(k) <= prioridade(pope.top()) and pope.top() != "(":
                    exppf.append(pope.pop())
                pope.push(k)
        # se k e operando (ultima opcao)    
        else: exppf.append(k)
    # desempilha todos os operadores que sobraram
    while not pope.is_empty():
        exppf.append(pope.pop())
    if pope.is_empty() != True or len(exppf) + a != b:
        return False
    return exppf

# ve se x e um numero ou uma variavel contida em listavar
# retorna o float do numero ou o elemento correspondente a "x" em listaval
def var_num(x):
    global listavar, listaval
    c = False
    for k in range(len(listavar)):
        if listavar[k] == x:
            x = listaval[k]
            c = True
    if c == False:
        x = float(x)
    return x

# -recebe uma lista
# -se tiver atribuicao: coloca a variavel e o valor nas listas 
# listavar e listaval, retorna o valo da atribuicao
# -se nao tiver atribuicao: printa o valor e o retorna
# -se der errado: retorna None
def CalcPosFixa(listaexp):
    global listavar, listaval
    operandos = PilhaLista()
    contr1 = False
    for k in listaexp:
        # se k e operador unario
        if prioridade(k) == 3:
            f = operandos.pop()
            try:
                f = var_num(f)
            except:
                print("Variavel nao declarada")
                #raise Invalid("Variavel nao declarada")
            if k == "_":
                f = -f
            operandos.push(f)
        # se k e operador binario != "="
        elif prioridade(k) != None and k != "=":
            # pega o ultimo item da pilha e pega seu valor
            a = operandos.pop()
            try:
                a = var_num(a)
            except:
                print("Variavel nao declarada")
                #raise Invalid("Variavel nao declarada")
            # pega o (pen)ultimo item da pilha e pega seu valor
            b = operandos.pop()
            try:
                b = var_num(b)
            except:
                print("Variavel nao declarada")
                #raise Invalid("Variavel nao declarada")        
            # checa qual operador e e faz a conta
            if k == "+":
                operandos.push(b+a)
            elif k == "-":
                operandos.push(b-a)
            if k == "*":
                operandos.push(b*a)
            if k == "/":
                operandos.push(b/a)
            if k == "^":
                operandos.push(b**a) 
        # se k e atribuicao (=)
        elif k == "=":
            # pega o ultimo item da pilha e pega seu valor
            c = (operandos.pop()) 
            try:
                c = var_num(c)
            except:
                print("Variavel nao declarada")
                #raise Invalid("Variavel nao declarada")
            # pega o (pen)ultimo item da pilha
            d = (operandos.pop()) 
            # adiciona ambos nas respectivas lista listaval e listavar
            # verificando antes se a variavel ja existe
            i = False
            for j in range(len(listavar)):
                if d == listavar[j]:
                    listaval[j] = float(c)
                    i = True
            if i == False:
                listavar.append(d)
                listaval.append(float(c))
            contr1 = True
        # se k e operando:
        else:
            if len(listaexp) == 1:
                try:
                    print(float(k), end="")
                    contr1 = True
                except:
                    contr2 = False
                    for t in range(len(listavar)):
                        if k == listavar[t]:
                           print(listaval[t], end="")
                           contr1 = True
                           contr2 = True
                    if contr2 == False:
                        print("Variavel nao declarada")
                        contr1 = True
            else:
                try:
                    operandos.push(float(k))
                except:
                    operandos.push(k)
    # se nao teve atribuicao
    # verifica se restou só um valor (resultado) 
    # e imprime na tela
    if contr1 == False:
        if len(operandos) != 1:
            return None
        l = False
        for p in range(len(listavar)):
            if operandos.top() == listavar[p]:
               print(listaval[p], end="")
               l= True
        if l == False:
            print(operandos.top(), end="")
        operandos.pop()
            
def main():
    while True:
        exp = str(input("\n>>> "))
        if Verifica_parentesis(exp):
            # arruma a expressao
            novo = arruma(exp)
            novo2 = arruma_unarios(novo)
            # traduz e calcula
            posfixa = TraduzPosFixa(novo2)
            try:
                CalcPosFixa(posfixa)
            except:
                print("Expressao invalida")
                #raise InvalidExpression("Expressao invalida")
        else:
            print("Os parenteses nao estao coerentes")
            print("Expressao invalida")
            #raise IncoerenciaParenteses("Os parenteses nao estao coerentes")


if __name__ == '__main__':
    main()