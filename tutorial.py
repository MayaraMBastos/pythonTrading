import json
import requests
import pandas as pd 
import datetime

par_moeda = "btcusd" #par da moeda que ira obter os dados
url = f"https://www.bitstamp.net/api/v2/ohlc/{par_moeda}/" #url da api para o get

start = "2021-01-01" # intervalo de inicio de datas
end  = "2021-01-02" # intervalo de final de datas

dates = pd.date_range(start, end, freq ="1H") #intervalo de tempo grafico
dates = [ int(x.value/10**9) for x in list(dates)] # lista de tempos em inteiro

print(dates)

master_data = []
for first, last in zip(dates, dates[1:]):
    print(first, last)

params = {
    "step":60, 
    "limit": 1000,
    "start": first,
    "end": last,
}

data = requests.get(url, params = params) # requerimento get com os parametros para a api

data = data.json()["data"]["ohlc"] #padrao de dados ohlc open high low e close

master_data += data

df = pd.DataFrame(master_data)
df = df.drop_duplicates()

df["timestamp"] = df["timestamp"].astype(int) #converte a coluna timestamp de string pra int
df = df.sort_values(by="timestamp") # ordena os valores

df = df [df["timestamp"] >= dates[0]]
df = df [df["timestamp"] < dates[-1]]
print(df)

df.to_csv("tutorial.csv", index=False) # sem os numeros de linhas/index