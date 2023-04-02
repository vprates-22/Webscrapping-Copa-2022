import pandas as pd

Atributos = tuple(["Data", "Partida", "Nome", "Nota", "Area", "Posição", "Min", "Gols", "Assist.", "Pênalti recebido", 
                "Total de chutes", "Chutes no gol", "Chutes para fora", "Trave", "Chutes interceptados", "Chances perdidas", 
                "Impedimentos", "Passes decisivos", "Quase gol", "Passes completados", "Passes longos completados", 
                "Cruzamentos completos", "Dribles completos", "Toques", "Faltas recebidas", "Pênalti cometido", "Faltas cometidas", 
                "Posse de bola perdida", "Driblado", "Perigo afastado", "Interceptações", "Bolas recuperadas", 
                "Vitória em duelos por baixo", "Vitória em duelos por cima", "Defesas", "Gols sofridos", "Pênalti defendido",
                "Reposição de soco", "Erros que terminaram em chute adversário", "Defesa pelo alto", "Seleção"])

a = pd.read_table("./data/def.txt", sep = ';', decimal=".",header=None, names=Atributos)
print(a.info())