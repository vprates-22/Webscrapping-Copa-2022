from selenium.webdriver.common.by import By
from time import sleep
import module_conv
import module
import json

URL = "https://www.365scores.com/pt-br/football/international/fifa-world-cup/league/5930/standings"
driver, actions = module.criaDriver(URL)

time_jog_sel = {}
times = set()
for grupo in range(8):
    for pos in range(2,6):
        sleep(1)
        sel = module_conv.acessa_pais(driver, actions, grupo, pos)
        module_conv.acessa_elenco(driver, actions)
        sleep(1)
        module_conv.coleta_jogadores(driver, sel, time_jog_sel, times)
        module.entreJogos(driver, actions)
driver.close()

with open("convocacao.json", "w") as file:
    json.dump(time_jog_sel, file, ensure_ascii=False)

with open("times.json", "w") as file:
    json.dump(list(times), file, ensure_ascii=False)