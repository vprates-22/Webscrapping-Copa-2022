from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from modules.module import criaDriver
from time import sleep
import json

def _clicaNoBuscar(driver:webdriver.Chrome, action:ActionChains) -> None:
    """
    Clica na lupinha para buscar um time
    Entrada: webdrive, ActionChains
    Saída: Nenhuma
    """
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div/div[1]/div[2]/button").click()

def _escreveNomeTime(action:ActionChains, Time:str) -> None:
    """
    Escreve o nome do time na barra de tarefas
    Entrada: ActionChains e nome do time a ser pesquisado
    Saída: Nenhuma
    """
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    action.send_keys(Time).perform()

def _escolheTime(driver:webdriver.Chrome, action:ActionChains) -> None:
    """
    Seleciona a opção futebol no filtro e acessa a 1° opção
    Entrada: webdrive, ActionChains
    Saída: Nenhuma
    """
    # clica na barra esporte
    sleep(0.5)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/div/div").click()
    # seleciona a opção futebol
    sleep(0.5)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/div[2]/span[1]").click()
    # clica na 1° opção
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/a/div[2]/div[1]").click()

def _acessaSecaoJogos(driver:webdriver.Chrome, action:ActionChains) -> None:
    """
    Acessa seção de jogos futuros do time
    Entrada: webdriver, ActionChains
    Saída: Nenhuma
    """
    try:
        # Tenta clicar na barra para descer as opções
        sleep(1)
        action.send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[1]/div/div/div/div/div/div").click()
    except:
        # Caso a página tenha tido algum problema de carregar o conteudo o
        # processo é reiniciado até a página carrgar tudo
        _acessaSecaoJogos(driver, action)
    try:
        # Seleciona a opção Jogos
        sleep(1)
        action.send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[1]/div/div/div/div/div[3]/a[1]").click()
    except:
        # Seleciona a opção Jogos, caso algum pop-up atrapalhe a tentativa anterior
        sleep(1)
        action.send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[1]/div/div/div/div/div[3]/a[1]").click()


def pesquisaTime(driver:webdriver.Chrome, action:ActionChains, Time:str) -> None:
    """
    Pesquisa o time e acessa a página de resultados daquele time
    Entrada: webdrive, ActionChains e nome do time a ser pesquisado
    Saída: Nenhuma
    """
    _clicaNoBuscar(driver, action)
    _escreveNomeTime(action, Time)
    _escolheTime(driver, action)
    _acessaSecaoJogos(driver, action)
    sleep(2)

def _apelidoJogo(driver:webdriver.Chrome, jogo:int) -> tuple:
    """
    Obtem o apelido dos times de um jogo
    Entrada: webdriver, int que representa o jogo
    Saída: tupla com apelido dos dois times (mandante, visitante)
    """
    # Verifica se está ocorrendo um jogo desse time
    status = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]").text
    if status != "Ao Vivo":
        # Coleta o mandante e visitante em caso de não haver jogo ao vivo
        mandante = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[3]/div[{jogo}]/div/div/div/div/div[2]/a/div[1]").text
        visitante = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[3]/div[{jogo}]/div/div/div/div/div[2]/a/div[3]").text
        if ":" in visitante or "Agr" in visitante:
            visitante = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[3]/div[{jogo}]/div/div/div/div/div[2]/a/div[4]").text
    else:
        # Coleta o mandante e visitante em caso de haver jogo ao vivo
        mandante = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[5]/div[{jogo}]/div/div/div/div/div[2]/a/div[1]").text
        visitante = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[5]/div[{jogo}]/div/div/div/div/div[2]/a/div[3]").text
    return mandante, visitante


def _coletaApelido(driver:webdriver.Chrome, actions:ActionChains, time:str) -> str:
    """
    Obtem o apelido do time em questão
    Entrada: webdriver, ActionChains, nome do time
    Saída: apelido do time(str)
    """
    pesquisaTime(driver, actions, time)
    dicio = {}
    prim = True # flag, sinaliza que passou da 1° iteração
    jogo = 1
    while True:
        a, b = _apelidoJogo(driver, jogo)
        jogo += 1
        
        # caso seja a 1° iteração, salvamos o nome dos dois times
        if prim:
            dicio[a] = 1 
            dicio[b] = 1
            prim = False
        # caso não seja a 1° iteração, tentamos descobrir o apelido do time
        else:
            # caso um dos apelidos coletados não for 
            # presente na 1° iteração ele não é quem procuramos
            # logo o outro é o apelido do time em questão
            flagA = dicio.get(a, 0)
            flagB = dicio.get(b, 0)
            if flagA and not flagB:
                return a
            if flagB and not flagA:
                return b

def apelidos(url:str, times:list, par:dict, inicio:int, final:int, file:str) -> None:
    """
    Realiza todo o processo de 
    Entrada: url a acessar,lista de times, par(dicionário -> nome: apelido), 
    inicio da iteração, final da iteração, arquivo para armazenar resultados
    Saída: Nenhuma
    """
    driver, action = criaDriver(url)
    for i in range(inicio, final):
        apelido = _coletaApelido(driver, action, times[i])
        par[times[i]] = apelido
    driver.close()
    # salva os apelidos coletados após (final - início) iterações
    json.dump(par, file, ensure_ascii=False)