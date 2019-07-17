import datetime
import requests
import json
import platform

#--------------------------------------------------------------------------------
# Contabilizei
# Data Engineer Technical Test
#--------------------------------------------------------------------------------
# Nome: util.py 
# Descricao: Script utilitario, aqui se encontram rotinas variadas.
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

URL_API = "https://api-sandbox.contabilizei.com/ds/customers"
ARQ_HIST_BUSCAS = "historico_buscas.json"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class consoleType:
    INFO = 0
    SUCCESS = 1
    ERROR = 2
    WARNING = 3

#----------------------------------------------------------
# Definicao de procedures 
#----------------------------------------------------------
           
def lerInteiro(msg):
    try:
        return int(input(msg).lower())
    except:
        return -1
        
def lerString(msg):
    return input(msg)

def writeConsole(msg,  type,  time = True):	
	sistema = platform.system()
	if sistema == "Linux":
		writeConsoleLinux(msg,  type,  time)
	else:
		writeConsoleOther(msg, time)
	
def writeConsoleLinux(msg,  type,  time):
    color = bcolors.ENDC
    if type == 0:
        color = bcolors.OKBLUE
    elif type == 1:
        color = bcolors.OKGREEN
    elif type == 2:
        color = bcolors.FAIL
    elif type == 3:
        color = bcolors.WARNING      
    if time:
        print(color+"[{0}] {1}".format(datetime.datetime.now(), msg)+bcolors.ENDC)
    else:
        print(color+"{0}".format(msg)+bcolors.ENDC)
	
def writeConsoleOther(msg, time):          
    if time:
        print("[{0}] {1}".format(datetime.datetime.now(), msg))
    else:
        print("{0}".format(msg))

def buscarEmpresas(product,  company_state):
    listaEmpresas = []
    arr = company_state.split(",")
    if len(arr) <= 1:
        buscarEmpresasAPI(listaEmpresas, product, company_state if company_state != "" else None)
    else:
        buscarEmpresasAPI(listaEmpresas, product, "{0},{1}".format(arr[0], arr[1]))
        buscarEmpresasAPI(listaEmpresas, product, "{0},{1}".format(arr[1], arr[0]))
    return listaEmpresas

def buscarEmpresasAPI(listaEmpresas, product,  company_state):
    if product == None:
        raise Exception("O parâmetro product não pode ser vazio") 
    query = "product=" + product if product != None else ""
    query += "&" if company_state != None and product != None else ""
    query += "company_state=" + company_state if company_state != None else ""
    url = URL_API + "?" + query
    response = requests.get(url)
    listDic = response.json()
    for dic in listDic:
        empresa = escreverEmpresa(dic, product)
        if empresa != None:
            listaEmpresas.append(empresa)
    
def escreverEmpresa(dicCostumer,  product_name):
    company_Id = dicCostumer["company_Id"]
    listState = dicCostumer["company_state"]
    state = ""
    for s in listState:
        state += s + ","
    state = state[:len(state)-1]
    listProduct = dicCostumer["Products_list"]
    for dicProduct in listProduct:
        company_Id = company_Id if company_Id != None else ""
        product = dicProduct["product"][0] if dicProduct["product"][0] != None else ""
        state = state if state != None else ""
        product_price =  dicProduct["product_price"] if dicProduct["product_price"] != None else ""
        line = "{0};{1};{2};{3}".format(product, company_Id, product_price, state)
        if product_name == product: 
            return line # desconsiderei casos em que ha repeticao do 'product' na 'Products_list', nesse caso pego a 1a ocorrencia
    return None
    
def gravarHistoricoBuscas(listHistBuscas):
    with open(ARQ_HIST_BUSCAS, 'w') as f:
        json.dump(listHistBuscas, f)

def lerHistoricoBuscas():
    with open(ARQ_HIST_BUSCAS, 'r') as f:
        return json.load(f)
