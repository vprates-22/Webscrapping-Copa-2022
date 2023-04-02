import modules.module_apelidos as module_apelidos
import json

# Arquivo que seram salvas chave: Nome / valor: Apelido usado pelo 365 scores
FILE_APELIDOS = "../data/nome_apelido.json"
FILE_TIMES = "../data/times.json"
URL = "https://www.365scores.com/pt-br"
# N° de times procurados por navegador
N_TIMES_POR_ITERACAO = 10

with open(FILE_APELIDOS) as file:
    TIME = json.load(file)

with open(FILE_APELIDOS, "r") as file:
    par = {}
    try:
        par = json.load(file)
    except:
        pass

N_TIMES = len(TIME)
QUOCIENTE = N_TIMES // N_TIMES_POR_ITERACAO
RESTO = N_TIMES % N_TIMES_POR_ITERACAO

for i in range(0, N_TIMES, N_TIMES_POR_ITERACAO):
    try:
        # Verifica se o bloco de N_TIMES_POR_ITERACAO já foi percorrido
        par[TIME[i]]
    except:
        # Caso o bloco não tenha sido percorrido se inicia o processo a pertir de par[time[i]]
        module_apelidos.apelidos(URL, TIME, par, i, i + N_TIMES_POR_ITERACAO, FILE_APELIDOS)
        
# Realiza o processo anterior para os RESTO times que sobraram
try:
    par[TIME[N_TIMES - RESTO]]
except:
    module_apelidos.apelidos(URL, TIME, par, N_TIMES - RESTO, N_TIMES, FILE_APELIDOS)