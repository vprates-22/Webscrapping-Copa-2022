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
                "Reposição de soco", "Erros que terminaram em chute adversário", "Defesa pelo alto"])
url = "https://www.365scores.com/pt-br"

with open("convocacao.json", "r") as file:
    convocados = json.load(file)

with open("times.json", "r") as file:
    Time = json.load(file)
Time = tuple(Time)

with open("nome_apelido.json") as file:
    apelidos = json.load(file)

driver, actions = module.criaDriver()
driver.get(url)
driver.find_element(By.XPATH, "//button[@id = 'didomi-notice-agree-button']").click()

for i in range(len(Time)):
    f_temp = open("a.txt", "w")
    for _ in range(3):
        opt = input(f"Deve coletar os dados do time {Time[i]} [Y/N]: ")
        if(opt == "Y"):
            module.pesquisaTime(driver, actions, Time[i])
            # Criando variáveis e configurações iniciais
            j=1
            while True:
                # Acessando um jogo específico
                dataLimite = datetime(2022, 8, 2)
                jogo, dataJogo = module.acessaJogo(driver, actions, j, dataLimite)
                if(jogo == 1):
                    resultado = module.acessaEscalação(driver, actions, apelidos[Time[i]])
                    module.acessaJogadores(driver, actions, f_temp, Atributos, [dataJogo, resultado])
                    module.entreJogos(driver, actions)
                    j += 1
                elif(jogo == 2):
                    j += 1
                else:
                    break
        else:
            continue
    driver.close()
    f_temp.close()
    module.adiciona()
    