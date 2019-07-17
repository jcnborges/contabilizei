import util
from util import writeConsole
from util import consoleType
import datetime
import os

#--------------------------------------------------------------------------------
# Contabilizei
# Data Engineer Technical Test
#--------------------------------------------------------------------------------
# Nome: main.py 
# Descricao: App principal.
# Autor:      
#       Julio Cesar B. da Silveira Nardelli - jcn.borges@gmail.com 
# Versao: 0.1
# Data: 2019-07-15
# Historico:
#       Versao 0.1: Criacao do codigo.
#--------------------------------------------------------------------------------

#----------------------------------------------------------
# Declaracao de constantes
#----------------------------------------------------------

TEMP_DIR = "./tmp/"

#----------------------------------------------------------
# Definicao de procedures 
#----------------------------------------------------------
def titulo():
    writeConsole("================================================",  consoleType.WARNING,  False)
    writeConsole("                Contabilizei                    ",  consoleType.WARNING,  False)
    writeConsole("       Data Engineer Technical Test             ",  consoleType.WARNING,  False)
    writeConsole("                    by                          ",  consoleType.WARNING,  False)
    writeConsole("     Júlio César B. da Silveira Nardelli        ",  consoleType.WARNING,  False)
    writeConsole("================================================",  consoleType.WARNING,  False)

def menuPrincipal():
    writeConsole("\nMenu de Opções:",  consoleType.WARNING,  False)
    writeConsole("1. Fazer nova busca.",  consoleType.WARNING,  False)
    writeConsole("2. Ver buscas anteriores.",  consoleType.WARNING,  False)
    writeConsole("3. Sair.",  consoleType.WARNING,  False)
    i = util.lerInteiro("Opção desejada: ")
    while i < 1 or i > 3:
        writeConsole("Opção inválida!",  consoleType.ERROR)
        i = util.lerInteiro("Opção desejada: ")
    return i

def fazerNovaBusca(listHistBuscas):
    writeConsole("=======================",  consoleType.WARNING,  False)
    writeConsole("    1. Nova busca      ",  consoleType.WARNING,  False)
    writeConsole("=======================",  consoleType.WARNING,  False)
    product = util.lerString("product = ")
    company_state = ""
    f = False
    while not f:
        try:
            company_state = util.lerString("company_state = ").replace(" ", "").upper()
            validarCompanyState(company_state)
            f = True
        except Exception as e: 
            writeConsole(str(e),  consoleType.ERROR)
    product = product if product != "" else None
    try:
        listEmpresas = util.buscarEmpresas(product, company_state)
        arquivo = gravarCSV(listEmpresas)
        consulta = {}
        consulta.update({"product":product})
        consulta.update({"company_state": company_state})
        consulta.update({"arquivo": arquivo})
        consulta.update({"time":datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")})
        consulta.update({"tamanho":len(listEmpresas)})
        listHistBuscas.append(consulta)
        util.gravarHistoricoBuscas(listHistBuscas)
        mostrarBusca(consulta)
    except Exception as  e:
        writeConsole(str(e),  consoleType.ERROR)

def validarCompanyState(company_state):
    arr = company_state.split(",")
    if len(arr) > 2:
        raise Exception("company_state inválido! (exemplos válidos: 'SP' ou 'SP,PR' ou vazio)")

def recuperarBuscasAnteriores(listHistBuscas):
    writeConsole("=======================",  consoleType.WARNING,  False)
    writeConsole(" 2. Buscas anteriores  ",  consoleType.WARNING,  False)
    writeConsole("=======================",  consoleType.WARNING,  False)
    n = 1
    for dic in reversed(listHistBuscas):
         writeConsole("{0}. Resultado da busca realizada por '{1}' e '{2}': {4} empresa(s) ({3})".format(n,  dic["product"],  dic["company_state"],  dic["time"],  dic["tamanho"]),  consoleType.WARNING,  False)
         n += 1
         if n > 3:
             break
    writeConsole("{0}. Voltar".format(n),  consoleType.WARNING,  False)
    i = util.lerInteiro("Opção desejada: ")
    while i < 1 or i > n:
        writeConsole("Opção inválida!",  consoleType.ERROR)
        i = util.lerInteiro("Opção desejada: ")
    if i < n:
        mostrarBusca(listHistBuscas[len(listHistBuscas)-i])
            
def mostrarBusca(dicBusca):
    if (dicBusca["tamanho"]  > 0):
        try:
            with open(dicBusca["arquivo"],  "r") as input:
                for linha in input:
                    writeConsole(linha.replace(";", "|").replace("\n",""),  consoleType.INFO,  False)
        except Exception as  e:
            writeConsole(str(e),  consoleType.ERROR)
    writeConsole("Resultado da busca realizada por '{0}' e '{1}': {3} empresa(s) ({2})".format(dicBusca["product"],  dicBusca["company_state"],  dicBusca["time"],  dicBusca["tamanho"]),  consoleType.SUCCESS,  False)
    if dicBusca["arquivo"] != None:
        writeConsole("Consulta gravada em {0}.".format(dicBusca["arquivo"]), consoleType.SUCCESS,  False)
 
def gravarCSV(listEmpresas):
    try:
        tamanho = len(listEmpresas)
        if tamanho == 0:
            return
        empresa = listEmpresas[0]
        nome = empresa.split(";")[1]
        arquivo = "{0}-{1}-{2}.csv".format(datetime.date.today().strftime("%d-%m-%y"), nome, tamanho)
        with open(TEMP_DIR + arquivo,  "w") as output:
            header = "product;company_Id;product_price;company_state\n"
            output.write(header)
            for empresa in listEmpresas:
                output.write(empresa+"\n")
        return TEMP_DIR + arquivo
    except Exception as  e:
        writeConsole(str(e),  consoleType.ERROR)
 
#----------------------------------------------------------
# Rotina principal
#----------------------------------------------------------
listHistBuscas = None
try:
    listHistBuscas = util.lerHistoricoBuscas()
except Exception as  e:
    listHistBuscas = []
    
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)
titulo()
i = 0
while i != 3:
    i = menuPrincipal()
    if i == 1: 
        fazerNovaBusca(listHistBuscas)
    elif i == 2:
        recuperarBuscasAnteriores(listHistBuscas)
writeConsole("Programa encerrado. Espero que tenham gostado!", consoleType.INFO,  False)
