from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep

def abre_pg():
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    return driver, ActionChains(driver)

def acessa_pais(driver, actions, grupo, pos):
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

def acessa_elenco(driver, actions):
    sleep(1)
    try:
        driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[2]/div[2]/a[5]/h2").click()
    except:
        try:
            driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[2]/div[2]/a[4]/h2").click()
        except:
            acessa_elenco(driver, actions)

def coleta_jogadores(driver, selecao, jog_sel, conj):
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

def retorna(driver, actions):
    driver.back()
    driver.back()
    actions.send_keys(Keys.ESCAPE).perform()