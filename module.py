from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from time import sleep
import selenium.common.exceptions as exc
import os

def criaDriver()->tuple:
    """Inicializa o webdriver
       Entrada: Nenhuma
       Saída: webdriver e ActionsChains"""
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    return driver, ActionChains(driver)

def pesquisaTime(driver:webdriver.Chrome, action:ActionChains, Time:str) -> None:
    """Pesquisa o time e acessa a página de resultados daquele time
       Entrada: webdrive, ActionChains e nome do time a ser pesquisado
       Saída: Nenhuma"""
    sleep(2)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div[1]/div[2]/button").click()
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    action.send_keys(Time).perform()
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/div/span").click()
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/div[2]/span[1]").click()
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/a/div[2]/div[1]").click()
    sleep(2)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[1]/div/div/div/div/div/span").click()
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[1]/div/div/div/div/div[3]/a[2]").click()
    sleep(1)

def tentaAcessarJogo(driver:webdriver.Chrome, action:ActionChains, jogo:int, lastDate:datetime, v=0) -> tuple:
    """Coleta a data do jogo, verifica se o jogo ocorreu após a data desejada e então acessa o jogo
       Entrada: webdriver, ActionChains, inteiro que representa o jogo, data limite
       Saída: uma flag, a data do jogo
       Significado das flags:
       0 -> jogo antes da data limite
       1 -> jogo ocorreu e dentro da data limite
       2 -> jogo não ocorreu"""
    action.send_keys(Keys.ESCAPE).perform()
    try:
        data = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/a/div[2]").text
    except:
        sleep(1)
        data = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/a/div[2]").text
    data = datetime.strptime(data, "%d/%m/%Y")
    if(data > lastDate):
        try:
            status = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/div/div/div/div/div[2]/a/div[2]").text
            if(status != "Fim" and status != "Placar pós-pênaltis" and status != "Pós-prorrog."):
                status = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/div/div/div/div/div[2]/a/div[3]").text
                if(status != "Fim" and status != "Placar pós-pênaltis" and status != "Pós-prorrog."):
                    return 2, data
            driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/div/div/div/div/div[2]/a").click()
        except:      
            action.send_keys(Keys.ESCAPE).perform()
            action.send_keys(Keys.HOME).perform()
            action.send_keys(v//2 * Keys.PAGE_DOWN).perform()
            sleep(1)
            if(v < 27):
                return tentaAcessarJogo(driver, action, jogo, lastDate, v+1)
            return tentaAcessarJogo(driver, action, jogo, lastDate, 0)
        return 1, data
    return 0, data

def acessaJogo(driver:webdriver.Chrome, action:ActionChains, jogo:int, lastDate:datetime) -> tuple:
    """Coleta a data do jogo, verifica se o jogo ocorreu após a data desejada e então acessa o jogo
       Entrada: webdriver, ActionChains, inteiro que representa o jogo, data limite
       Saída: uma flag, a data do jogo
       Significado das flags:
    0 -> jogo antes da data limite
    1 -> jogo ocorreu e dentro da data limite
    2 -> jogo não ocorreu"""
    return tentaAcessarJogo(driver, action, jogo, lastDate)

def tentaAcessaEscalação(driver:webdriver.Chrome, Time:str) -> str:
    """Acessa a escalação detalhada e adentra o time em questão
       Entrada: webdriver, nome do time
       Saida: resultado do jogo"""
    sleep(0.5)
    resultado = driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[3]/div/div[1]").text.split("\n")
    driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[3]/div/div[2]/div[8]/div/div[2]/a").click()
    sleep(0.5)
    Home = driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[1]/div/div[1]")
    if(Home.text == Time):
        Home.click()
        sleep(0.5)
    else:
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[1]/div/div[2]").click()
        sleep(0.5)
    return resultado[0] + " " + resultado[2] + "x" + resultado[4] + " " + resultado[6]

def acessaEscalação(driver:webdriver.Chrome, action:ActionChains, Time:str, i=0) -> str:
    """Acessa a escalação detalhada e adentra o time em questão
       Entrada: webdriver, nome do time
       Saida: resultado do jogo"""
    try:
        sleep(1)
        action.send_keys(Keys.ESCAPE).perform()
        action.send_keys(Keys.HOME).perform()
        action.send_keys(i//3 * Keys.PAGE_DOWN).perform()
        sleep(0.5)
        return tentaAcessaEscalação(driver, Time)
    except:
        if(i>9):
            driver.back()
            sleep(1)
            driver.forward()
            sleep(1)
            return acessaEscalação(driver, action, Time, 0)
        return acessaEscalação(driver, action, Time, i+1)

def acessaJogadores(driver:webdriver.Chrome, action:ActionChains, file, atributos:tuple, dadosJogo:list)-> None:
    """Acessa os jogadores, coleta e escreve os dados em um arquivo
       Entrada: webdriver, ActionChains, arquivo, lista de atributos, lista com [data do jogo, resultado do jogo]
       Saida: Nenhuma"""
    try:
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/span[1]/div/div/div[2]/div[2]").click()
        sleep(1)
    except:
        sleep(1)
        action.send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/span[1]/div/div/div[2]/div[2]").click()
        sleep(1)
    i = 0
    for _ in range(1,18):
        try:
            driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div").text
            coletaDados(driver, file, atributos, dadosJogo)
            action.send_keys(Keys.RIGHT).perform()
            i += 1
        except exc.NoSuchElementException:
            try:
                driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div").text
                coletaDados(driver, file, atributos, dadosJogo, 1)
                action.send_keys(Keys.RIGHT).perform()
                i += 1
            except:
                if(i<11):
                    driver.back()
                    driver.forward()
                    acessaJogadores(driver, action, file, atributos, dadosJogo)
                break
    
def entreJogos(driver:webdriver.Chrome, action:ActionChains)->None:
    """Retorna à página de resultados
       Entrada: webdriver, ActionChains
       Saida: Nenhuma"""
    driver.back()
    driver.back()
    sleep(0.5)
    action.send_keys(Keys.ESCAPE).perform()

def coletaInicial(driver:webdriver.Chrome, alt = 0)->dict:
    """Acessa a escalação detalhada e adentra o time em questão
       Entrada: webdriver, flag
       Saida: dicionário com Nome, Posiçã, Nota"""
    stats = {}
    if alt == 0:
        stats["Nome"] = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]").text
        nota = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div").text
        stats["Posição"] = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[2]").text
    
    else:
        stats["Nome"] = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[1]/div[2]/div[1]/div[1]").text
        nota = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div").text
        stats["Posição"] = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[1]/div[2]/div[2]").text
    
    if("-" != nota):
        stats["Nota"] = nota

    return stats

def escreveDados(file, dados:dict, atributos:tuple, dadosJogo:list)->None:
    """Recebe um dicionário e escreve de maneira formatada no arquivo
       Entrada: arquivo, dicionário de dados, lista de atributos, lista com [data do jogo, resultado do jogo]
       Saida: Nenhuma"""
    file.write(dadosJogo[0].strftime("%d/%m/%Y") + ";" + dadosJogo[1])
    for i in atributos[2:]:
        try:
            file.write(';' + dados[i])
        except KeyError:
            file.write(';')
    file.write("\n") 

def coletaDados(driver:webdriver.Chrome, file, atributos:tuple, dadosJogo:list, alt = 0)->None:
    """Coleta as estatisticas de cada jogador
       Entrada: webdriver, arquivo, lista de atributos, lista com [data do jogo, resultado do jogo]
       Saida: Nenhuma"""
    if alt == 0:
        stats = coletaInicial(driver)
        primeiroBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[2]/div[1]").text.split("\n")
        segundoBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[2]/div[2]").text.split("\n")
        terceiroBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[2]/div[3]").text.split("\n")
    else:
        stats = coletaInicial(driver, alt)
        primeiroBloco = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[2]/div[1]").text.split("\n")
        segundoBloco = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[2]/div[2]").text.split("\n")
        terceiroBloco = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[2]/div[3]").text.split("\n")

    stats[primeiroBloco[2]] = primeiroBloco[1][:-1]
    stats[primeiroBloco[4]] = primeiroBloco[3][0]
    stats[primeiroBloco[6]] = primeiroBloco[5]
    stats['Area'] =  segundoBloco[0]
    for i in range(1, len(segundoBloco), 2):
        stats[segundoBloco[i]] = segundoBloco[i+1]
    for i in range(1, len(terceiroBloco), 2):
        if(terceiroBloco[i] != "Assistências"):
            stats[terceiroBloco[i]] = terceiroBloco[i+1]
        else:
            stats["Assist."] = terceiroBloco[i+1]
    escreveDados(file, stats, atributos, dadosJogo)

def adiciona()->None:  
    """Transcreve os dados obtidos do arquivo temporário até o definitivo
       Entrada: Nenhuma
       Saída: Nenhuma"""  
    f_temp = open("a.txt", "r")
    f_def = open("def.txt", "a")
    for i in f_temp:
        f_def.write(i)
    f_temp.close()
    f_def.close()
    os.remove("a.txt")