import json
import module_conv
import module

def coleta_apelido(driver:module_conv.webdriver.Chrome, actions:module_conv.ActionChains, time:str):
    module.pesquisaTime(driver, actions, time)
    module.sleep(2)
    for i in range(1, 10):
        if i%2 == 1:
            dicio = {}
            prim = True

        try:
            a = driver.find_element(module.By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{i}]/div/div/div/div/div[2]/a/div[1]").text
        except:
            module.sleep(10)
            actions.send_keys(module.Keys.ESCAPE).perform()
            a = driver.find_element(module.By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{i}]/div/div/div/div/div[2]/a/div[1]").text

        b = driver.find_element(module.By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{i}]/div/div/div/div/div[2]/a/div[4]").text
        if "\n-" in b:
            b = driver.find_element(module.By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{i}]/div/div/div/div/div[2]/a/div[5]").text
        
        if prim:
            dicio[a] = 1 
            dicio[b] = 1
            prim = False
        else:
            try:
                dicio[a]
                return a
            except:
                try:
                    dicio[b]
                    return b
                except:
                    continue

with open("times.json") as file:
    times = json.load(file)

url = "https://www.365scores.com/pt-br"

with open("apelidos.json", "r") as file:
    par = json.load(file)
i = 0
for _ in range(len(times)//10):
    try:
        par[times[i]]
        i+=10
    except:
        driver, action = module_conv.abre_pg()
        driver.get(url)
        driver.find_element(module.By.XPATH, "//button[@id = 'didomi-notice-agree-button']").click()
        for _ in range(10):
            apelido = coleta_apelido(driver, action, times[i])
            par[times[i]] = apelido
            print(apelido)
            i += 1
        driver.close()
    with open("apelidos.json", "w") as file:
        json.dump(par, file, ensure_ascii=False)

driver, action = module_conv.abre_pg()
driver.get(url)
driver.find_element(module.By.XPATH, "//button[@id = 'didomi-notice-agree-button']").click()
for _ in range(len(times)%10):
    apelido = coleta_apelido(driver, action, times[i])
    par[times[i]] = apelido
    i += 1
    print(apelido)
driver.close()

with open("nome_apelido.json", "w") as file:
    json.dump(par, file, ensure_ascii=False)