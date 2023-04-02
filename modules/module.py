from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exc
from selenium import webdriver
from datetime import datetime
from modules.module_apelidos import liberaCookies
from time import sleep
import os

def liberaCookies(driver:webdriver.Chrome) -> None:
    """
    Concorda com os cookies da página ao abrirmos a página
    Entrada: webdrive
    Saída: Nenhuma
    """
    try:
        sleep(2)
        # clica no butão de aceitar os cookies
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]").click()
    except:
        sleep(2)
        liberaCookies(driver)

def criaDriver(url:str) -> tuple:
    """
    Inicializa o webdriver, o ActionsChains, acessa a página da url e aceita os cookies
    Entrada: Nenhuma
    Saída: webdriver e ActionsChains
    """
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    liberaCookies(driver)
    sleep(2)
    return driver, ActionChains(driver)

def _coletaDataECampeonato(driver:webdriver.Chrome, action:ActionChains, jogo:int) -> tuple:
    """
    Coleta a data e o campeonato do jogo 
    Entrada: webdrive, ActionChains e inteiro que representa o jogo
    Saída: Nenhuma
    """
    action.send_keys(Keys.ESCAPE).perform()
    action.send_keys(Keys.END).perform()
    sleep(1)
    # coleta a data do jogo
    data = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/a/div[2]").text
    # coleta qual é o campeonato do jogo
    campeonato = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/a/div[1]/div/div[1]").text
    # tranforma a string data em um objeto de datatime, tornando possível comparar datas
    data = datetime.strptime(data, "%d/%m/%Y")
    return data, campeonato

def _verifJogoNaoRealizado(driver:webdriver.Chrome, jogo:int, v:int = 2) -> bool:
    """
    Verifica se jogo não foi realizado
    Entrada: webdrive, ActionChains e inteiro que representa o jogo
    Saída: booleano
    """
    # coleta o status do jogo(Fim, Placar pós-pênaltis, etc)
    status = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/div/div/div/div/div[2]/a/div[{v}]").text
    return status != "Fim" and status != "Placar pós-pênaltis" and status != "Pós-prorrog."

def _descePagina(action:ActionChains, v:int, k:int) -> None:
    """
    Desce a página v//k vezes
    Entrada: ActionChains e um inteiro v
    Saída: 
    """
    sleep(1)
    action.send_keys(Keys.ESCAPE).perform()
    action.send_keys(Keys.HOME).perform()
    action.send_keys(v//k * Keys.PAGE_DOWN).perform()

def _tentaAcessarJogo(driver:webdriver.Chrome, action:ActionChains, jogo:int, lastDate:datetime, blacklist:tuple, v=0) -> tuple:
    """
    Coleta a data do jogo, verifica se o jogo ocorreu após a data desejada e então acessa o jogo
    Entrada: webdriver, ActionChains, inteiro que representa o jogo, data limite
    Saída: uma flag, a data do jogo
    Significado das flags:
    0 -> jogo antes da data limite
    1 -> jogo ocorreu e dentro da data limite
    2 -> jogo não ocorreu
    """
    data, campeonato = _coletaDataECampeonato(driver, action, jogo)
    if data > datetime(2022, 11, 18) or campeonato in blacklist:
        return 2, data
    if data > lastDate:
        try:
            if _verifJogoNaoRealizado(driver, jogo):
                if _verifJogoNaoRealizado(driver, jogo, 3):
                    return 2, data
            # clica no jogo
            driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/div/div/div/div/div[2]/a").click()
        except:      
            _descePagina(action, v, 2)
            if(v < 27):
                return _tentaAcessarJogo(driver, action, jogo, lastDate, blacklist, v+1)
            return _tentaAcessarJogo(driver, action, jogo, lastDate, blacklist, 0)
        return 1, data
    return 0, data

def acessaJogo(driver:webdriver.Chrome, action:ActionChains, jogo:int, lastDate:datetime, blacklist:tuple) -> tuple:
    """
    Coleta a data do jogo, verifica se o jogo ocorreu após a data desejada e então acessa o jogo
    Entrada: webdriver, ActionChains, inteiro que representa o jogo, data limite
    Saída: uma flag, a data do jogo
    Significado das flags:
    0 -> jogo antes da data limite
    1 -> jogo ocorreu e dentro da data limite
    2 -> jogo não ocorreu
    """
    try:
        return _tentaAcessarJogo(driver, action, jogo, lastDate, blacklist)
    except:
        return _tentaAcessarJogo(driver, action, jogo, lastDate, blacklist)

def _selecionaLado(driver:webdriver.Chrome, Time:str) -> None:
    """
    Escolhe qual time é o que devemos coletar os dados
    Entrada: webdriver, nome do time
    Saída: Nenhuma
    """
    # botão do time mandante
    Home = driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[1]/div/div[1]")
    if(Home.text == Time):
        Home.click()
    else:
        # botão do time visitante
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[1]/div/div[2]").click()
    sleep(0.5)

def _tentaAcessaEscalação(driver:webdriver.Chrome, Time:str) -> str:
    """
    Acessa a escalação detalhada e adentra o time em questão
    Entrada: webdriver, nome do time
    Saida: resultado do jogo
    """
    sleep(0.5)
    # placar do jogo
    resultado = driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[3]/div/div[1]").text.split("\n")
    # expande a escalação dos times
    driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[3]/div/div[2]/div[8]/div/div[2]/a").click()
    sleep(0.5)
    _selecionaLado(driver, Time)
    return resultado[0] + " " + resultado[2] + "x" + resultado[4] + " " + resultado[6]

def acessaEscalação(driver:webdriver.Chrome, action:ActionChains, Time:str, i=0) -> str:
    """
    Acessa a escalação detalhada e adentra o time em questão
    Entrada: webdriver, nome do time
    Saida: resultado do jogo
    """
    try:
        _descePagina(action, i, 3)
        return _tentaAcessaEscalação(driver, Time)
    except:
        if(i>9):
            driver.refresh()
            sleep(2)
            return acessaEscalação(driver, action, Time, 0)
        return acessaEscalação(driver, action, Time, i+1)

def _obtemJogador(driver:webdriver.Chrome, action:ActionChains, file, atributos:tuple,
                   dadosJogo:list, time:str, convocacao:dict, nome:str, flag:int = 0) -> None:
    """
    Acessa um jogador, coleta e passa para o próximo
    Entrada: webdriver, ActionChains, arquivo, lista de atributos, 
    lista com [data do jogo, resultado do jogo], nome do jogador, flag
    Saida: Nenhuma
    """
    if convocacao[time].get(nome, 0):
        coletaDados(driver, file, atributos, dadosJogo, convocacao[time][nome], flag)
        action.send_keys(Keys.RIGHT).perform()
    else:
        action.send_keys(Keys.RIGHT).perform()

def _clicaNoPrimeiroJogador(driver:webdriver.Chrome, action:ActionChains) -> None:
    """
    Acessa o 1° jogador do time
    Entrada: webdriver, ActionChains
    Saída: Nenhuma
    """
    try:
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/span[1]/div/div/div[2]/div[2]").click()
        sleep(1)
    except:
        sleep(1)
        action.send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/span[1]/div/div/div[2]/div[2]").click()
        sleep(1)

def _tentaNovamente(driver:webdriver.Chrome, action:ActionChains) -> None:
    """
    Reabre a mesma página
    Entrada: webdriver, ActionChains
    Saída: Nenhuma
    """
    action.send_keys(Keys.ESCAPE).perform()
    driver.back()
    sleep(1)
    driver.forward()
    sleep(1)

def acessaJogadores(driver:webdriver.Chrome, action:ActionChains, file, 
                    atributos:tuple, dadosJogo:list, time:str, convocacao:dict)-> None:
    """
    Acessa os jogadores, coleta e escreve os dados em um arquivo
    Entrada: webdriver, ActionChains, arquivo, lista de atributos, lista com [data do jogo, resultado do jogo]
    Saida: Nenhuma
    """
    _clicaNoPrimeiroJogador(driver, action)
    i = 0
    for _ in range(1,18):
        try:
            # verifica se o jogador jogou acessando um campo que apenas um jogador que ntrou possui
            driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div[3]")
            nome = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]").text
            _obtemJogador(driver, action, file, atributos, dadosJogo, time, convocacao, nome)
            i += 1
        except exc.NoSuchElementException:
            if(i<2):
                _tentaNovamente(driver, action)
                _selecionaLado(driver, time)
                acessaJogadores(driver, action, file, atributos, dadosJogo, time, convocacao)
            break
"""            try:
                # verifica se o jogador jogou acessando um campo que apenas um jogador que ntrou possui
                driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__osART modal_modal_root__nugMg direction-ltr']/div/div[2]/div/div[2]/div[3]")
                nome = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__osART modal_modal_root__nugMg direction-ltr']/div/div[2]/div/div[1]/div[2]/div[1]/div[1]").text
                _obtemJogador(driver, action, file, atributos, dadosJogo, time, convocacao, nome, 1)
                i += 1
            except exc.NoSuchElementException:"""
    
def entreJogos(driver:webdriver.Chrome, action:ActionChains)->None:
    """
    Retorna à página de resultados
    Entrada: webdriver, ActionChains
    Saida: Nenhuma
    """
    driver.back()
    driver.back()
    sleep(0.5)
    action.send_keys(Keys.ESCAPE).perform()

def _coletaInicial(driver:webdriver.Chrome, alt = 0)->dict:
    """
    Acessa a escalação detalhada e adentra o time em questão
    Entrada: webdriver, flag
    Saida: dicionário com Nome, Posiçã, Nota
    """
    stats = {}

    stats["Nome"] = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]").text
    nota = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div").text
    stats["Posição"] = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[2]").text

    if("-" != nota):
        stats["Nota"] = nota

    return stats
    
#    if alt == 0:
#    else:
#        stats["Nome"] = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[1]/div[2]/div[1]/div[1]").text
#        nota = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div").text
#        stats["Posição"] = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[1]/div[2]/div[2]").text
    

def escreveDados(file, dados:dict, atributos:tuple, dadosJogo:list)->None:
    """
    Recebe um dicionário e escreve de maneira formatada no arquivo
    Entrada: arquivo, dicionário de dados, lista de atributos, lista com [data do jogo, resultado do jogo]
    Saida: Nenhuma
    """
    file.write(dadosJogo[0].strftime("%d/%m/%Y") + ";" + dadosJogo[1])
    for i in atributos[2:]:
        try:
            file.write(';' + dados[i])
        except KeyError:
            file.write(';')
    file.write("\n") 

def coletaDados(driver:webdriver.Chrome, file, atributos:tuple, 
                dadosJogo:list, selecao:str, alt = 0)->None:
    """
    Coleta as estatisticas de cada jogador
    Entrada: webdriver, arquivo, lista de atributos, lista com [data do jogo, resultado do jogo]
    Saida: Nenhuma
    """
    stats = _coletaInicial(driver)
    primeiroBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[2]/div[1]").text.split("\n")
    segundoBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[2]/div[2]").text.split("\n")
    terceiroBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[2]/div[3]").text.split("\n")
 
    stats[primeiroBloco[2]] = primeiroBloco[1][:-1]
    stats[primeiroBloco[4]] = primeiroBloco[3][0]
    stats[primeiroBloco[6]] = primeiroBloco[5]
    stats['Area'] =  segundoBloco[0]
    stats['Seleção'] = selecao
    for i in range(1, len(segundoBloco), 2):
        stats[segundoBloco[i]] = segundoBloco[i+1]
    for i in range(1, len(terceiroBloco), 2):
        if(terceiroBloco[i] != "Assistências"):
            stats[terceiroBloco[i]] = terceiroBloco[i+1]
        else:
            stats["Assist."] = terceiroBloco[i+1]
    escreveDados(file, stats, atributos, dadosJogo)
#    if alt == 0:
#    else:
#        stats = _coletaInicial(driver, alt)
#        segundoBloco = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[2]/div[2]").text.split("\n")
#        terceiroBloco = driver.find_element(By.XPATH, "//html/body/div[4]/div[@class='scores365 modal_show__2QSda modal_modal_root___VpbK direction-ltr']/div/div[2]/div/div[2]/div[3]").text.split("\n")


def adiciona()->None:  
    """
    Transcreve os dados obtidos do arquivo temporário até o definitivo
    Entrada: Nenhuma
    Saída: Nenhuma
    """  
    f_temp = open("../data/a.txt", "r")
    f_def = open("../data/def.txt", "a")
    for i in f_temp:
        f_def.write(i)
    f_temp.close()
    f_def.close()
    os.remove("../data/a.txt")