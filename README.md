# Webscrapping-Copa-2022
## Webscarpping das Estatísticas
### Diretório scrapping
arquivo "apelidos.py" - coleta os apelidos de cada time - resultados salvo em "data/nome_apelidos.json"
arquivo "convocação.py" - coleta os jogadores convocados de cada seleção e seus respectivos times- resultados salvo em "data/convocacao.json" e "data/times.json"
arquivo "webscrapper.py" - coleta de dados dos jogadores convocados - resultados salvos em "data/def.txt"

## Modularização do código
### Diretório modules
arquivo "module_apelidos.py" - modulo das principais funções de "scrapping/apelidos.py"
arquivo "module_conv.py" - modulo das principais funções de "scrapping/convocacao.py"
arquivo "module.py" - modulo das principais funções de "scrapping/webscrapper.py"

## Armazem de dados
### Diretório data
arquivo "convocacao.json" - contem uma estrutura de dicionário {time: {jogador : seleção}}
arquivo "nome_apelidos.json" - contem uma estrutura de dicionário {nome completo time : apelido time} 
arquivo "time.json" - contem uma estrutura de lista com o nome completo de cada time que contem um jogador convocado
arquivo "def.txt" - contem o dado de quase todos os jogadores convocados entre 05/08/2022 até o início da Copa do Mundo de 2022
arquivo "leituras" - contem 

## Análise dos dados
### main.ipynb (Incompleto)