from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

def acessa_pais(driver:webdriver.Chrome, actions:ActionChains, grupo:int, pos:int) -> str:
    """
    Entra na página de um páis que disputou a copa do mundo
    Entrada: webdriver, ActionChains, int que representa o grupo, int que representa a posição na classificação
    Saída: nome da seleção
    """
    try:
        actions.send_keys(Keys.ESCAPE).perform()
        sleep(1)
        link = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div/div[1]/div[{2 * (grupo + 1)}]/table/tbody/tr[{pos}]/td[3]/a/div")
        selecao = link.text
        link.click()
        print(selecao)
        return selecao
    except :
        actions.send_keys(Keys.PAGE_DOWN).perform()
        sleep(1)
        return acessa_pais(driver, actions, grupo, pos)

def acessa_elenco(driver:webdriver.Chrome, actions:ActionChains) -> None:
    """
    Entra na seção elenco
    Entrada: webdriver, ActionsChains
    Saída: Nenhuma
    """
    sleep(1)
    try:
        driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[2]/div[2]/a[5]/h2").click()
    except:
        try:
            driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[2]/div[2]/a[4]/h2").click()
        except:
            acessa_elenco(driver, actions)

def coleta_jogadores(driver:webdriver.Chrome, selecao:str, jog_sel:dict, conj:set) -> None:
    """
    Coleta todos os 26 atletas convocados pela seleção em questão
    Entrada: webdriver, nome da seleção, dicionário (key: time/value: dict(key:time/value:seleção))
    Saída: Nenhuma
    """
    for play in range(2, 28):
        try:
            dados_jog = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div/a[{play}]").text
            dados_jog = dados_jog.split("\n")
            nome = dados_jog[0]
            time = dados_jog[1].split('(')[0]
            try: 
                jog_sel[time]
            except:
                jog_sel[time] = {}
            conj.add(time)
            jog_sel[time][nome] = selecao
        except:
            break    