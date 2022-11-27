from selenium.webdriver.common.by import By
from datetime import datetime
import json
import module

Atributos = tuple(["Data", "Partida", "Nome", "Nota", "Area", "Posição", "Min", "Gols", "Assist.", "Pênalti recebido", 
                "Total de chutes", "Chutes no gol", "Chutes para fora", "Trave", "Chutes interceptados", "Chances perdidas", 
                "Impedimentos", "Passes decisivos", "Quase gol", "Passes completados", "Passes longos completados", 
                "Cruzamentos completos", "Dribles completos", "Toques", "Faltas recebidas", "Pênalti cometido", "Faltas cometidas", 
                "Posse de bola perdida", "Driblado", "Perigo afastado", "Interceptações", "Bolas recuperadas", 
                "Vitória em duelos por baixo", "Vitória em duelos por cima", "Defesas", "Gols sofridos", "Pênalti defendido",
                "Reposição de soco", "Erros que terminaram em chute adversário", "Defesa pelo alto", "Seleção"])
url = "https://www.365scores.com/pt-br"

blacklist = tuple(["Amistoso", "Copa da Bélgica", "Leagues Cup", "Copa da França",
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
Time = tuple(Time)

with open("nome_apelido.json") as file:
    apelidos = json.load(file)


with open("leituras.json") as file:
    lidos = json.load(file)

i = 0
for _ in range(len(Time)):
    try:
        lidos[Time[i]]
        i += 1
    except:
        driver, actions = module.criaDriver()
        driver.get(url)
        driver.find_element(By.XPATH, "//button[@id = 'didomi-notice-agree-button']").click()
        module.sleep(2)
        for a in range(3):
            f_temp = open("a.txt", "w")
            module.pesquisaTime(driver, actions, Time[i])
            # Criando variáveis e configurações iniciais
            j=1
            while True:
                # Acessando um jogo específico
                dataLimite = datetime(2022, 8, 4)
                jogo, dataJogo = module.acessaJogo(driver, actions, j, dataLimite, blacklist)
                if(jogo == 1):
                    resultado = module.acessaEscalação(driver, actions, apelidos[Time[i]])
                    module.acessaJogadores(driver, actions, f_temp, Atributos, [dataJogo, resultado], Time[i], convocados)
                    module.entreJogos(driver, actions)
                    j += 1
                elif(jogo == 2):
                    j += 1
                else:
                    break
                lidos[Time[i]] = "Lido"
            i += 1
            f_temp.close()
            module.adiciona()
            with open("leituras.json", "w") as file:
                json.dump(lidos, file, ensure_ascii=False)
        driver.close()
