from datetime import datetime
import module_apelidos
import module
import json

URL = "https://www.365scores.com/pt-br"

ATRIBUTOS = tuple(["Data", "Partida", "Nome", "Nota", "Area", "Posição", "Min", "Gols", "Assist.", "Pênalti recebido", 
                "Total de chutes", "Chutes no gol", "Chutes para fora", "Trave", "Chutes interceptados", "Chances perdidas", 
                "Impedimentos", "Passes decisivos", "Quase gol", "Passes completados", "Passes longos completados", 
                "Cruzamentos completos", "Dribles completos", "Toques", "Faltas recebidas", "Pênalti cometido", "Faltas cometidas", 
                "Posse de bola perdida", "Driblado", "Perigo afastado", "Interceptações", "Bolas recuperadas", 
                "Vitória em duelos por baixo", "Vitória em duelos por cima", "Defesas", "Gols sofridos", "Pênalti defendido",
                "Reposição de soco", "Erros que terminaram em chute adversário", "Defesa pelo alto", "Seleção"])

BLACKLIST = tuple(["Amistoso", "Copa da Bélgica", "Leagues Cup", "Copa da França",
                   "Copa da Grécia", "Copa da Croácia", "Copa da Inglaterra", 
                   "Copa Ecuador", "Copa do Rei", "Taça da Liga",
                   "Copa da Turquia", "Copa da Polônia", "Taça de Portugal",
                   "Copa da Rússia", "Copa da Suíça", "Copa da Colômbia",
                   "Copa da Liga do Japão", "Copa da Áustria", "Copa da Dinamarca",
                   "Liga dos Campeões da CAF", "Copa do Egito", "Copa da Holanda",
                   "Liga dos Campeões Q."])

with open("convocacao.json", "r") as file:
    convocados = json.load(file)

with open("times.json", "r") as file:
    Time = json.load(file)
TIME = tuple(Time)

with open("nome_apelido.json") as file:
    APELIDOS = json.load(file)

with open("leituras.json") as file:
    lidos = json.load(file)

i = 0
for _ in range(len(TIME)):
    try:
        lidos[TIME[i]]
        i += 1
    except:
        driver, actions = module.criaDriver(URL)
        for a in range(3):
            f_temp = open("a.txt", "w")
            module_apelidos.pesquisaTime(driver, actions, TIME[i])
            # Criando variáveis e configurações iniciais
            j=1
            while True:
                # Acessando um jogo específico
                dataLimite = datetime(2022, 8, 4)
                jogo, dataJogo = module.acessaJogo(driver, actions, j, dataLimite, BLACKLIST)
                if(jogo == 1): # jogo realizado, logo se deve coletar os dados
                    resultado = module.acessaEscalação(driver, actions, APELIDOS[TIME[i]])
                    module.acessaJogadores(driver, actions, f_temp, ATRIBUTOS, [dataJogo, resultado], TIME[i], convocados)
                    module.entreJogos(driver, actions)
                    j += 1
                elif(jogo == 2): # jogo adiado 
                    j += 1
                else: # jogo realizado antes da dataLimite
                    break
            i += 1
            lidos[Time[i]] = "Lido" # sinaliza que time já foi coletado completamente
            f_temp.close()
            module.adiciona()
            with open("leituras.json", "w") as file:
                json.dump(lidos, file, ensure_ascii=False)
        driver.close()