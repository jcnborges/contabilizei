import util
#--------------------------------------------------------------------------------
# Contabilizei
# Data Engineer Technical Test
#--------------------------------------------------------------------------------
# Nome: unit_test.py 
# Descricao: Bateria de testes unitários.
# Autor:      
#       Julio Cesar B. da Silveira Nardelli - jcn.borges@gmail.com 
# Versao: 0.1
# Data: 2019-07-16
# Historico:
#       Versao 0.1: Criacao do codigo.
#--------------------------------------------------------------------------------
print("\nBusca simples")
lista = util.buscarEmpresas("water", "")
for l in lista:
    print(l)

print("\nBusca 1 estado")
lista = util.buscarEmpresas("coca", "SP")
for l in lista:
    print(l)

print("\nBusca 2 estados")
lista = util.buscarEmpresas("water", "PR,RJ") # a ordem não pode influenciar 'PR,RJ' = 'RJ,PR'
for l in lista:
    print(l)

print("\nBusca vazia")
lista = util.buscarEmpresas("michael jackson", "EUA") # a ordem não pode influenciar 'PR,RJ' = 'RJ,PR'
for l in lista:
    print(l)

print("\nInput com erro")
try:    
    lista = util.buscarEmpresas(None, "")
except Exception as e:
    print(e)
    

