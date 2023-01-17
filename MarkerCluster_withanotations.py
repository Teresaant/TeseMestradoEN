#%%

import plotly.express as px
import plotly
import pandas as pd
import folium
from folium import plugins
from folium.plugins import MarkerCluster

# Converter as coordenas em graus em valores decimal
# Referência:
# https://stackoverflow.com/questions/10852955/python-batch-convert-gps-positions-to-lat-lon-decimals
def conversion(old):
    direction = {"N": 1, "S": -1, "E": 1, "W": -1}
    new = old.replace("°", " ").replace("'", " ").replace('"', " ")
    new = new.split()
    new_dir = new.pop()
    new.extend([0, 0, 0])
    return (int(new[0]) + int(new[1]) / 60.0 + int(new[2]) / 3600.0) * direction[
        new_dir
    ]

df2017 = pd.read_csv("dados-2017.csv")
df2018 = pd.read_csv("dados-2018.csv")
df2019 = pd.read_csv("dados-2019.csv")
df2020 = pd.read_csv("dados-2020.csv")
df2021 = pd.read_csv("dados-2021.csv")

# Acrescenta a cada data frame as colunas latitude e longitude
for d in [df2017, df2018, df2019, df2020, df2021]:
    d["lat"] = d.apply(lambda row: conversion(row["coordenadas"].split()[0]), axis=1)
    d["lon"] = d.apply(lambda row: conversion(row["coordenadas"].split()[1]), axis=1)

# Junta os dados dos vários anos
df = pd.concat([df2017, df2018, df2019, df2020, df2021])

#Heatmaps só funcionam com listas de listas, por isso devemos converter as data frames
heat_df = df[['lat', 'lon']]
heat_data = heat_df.values.tolist()

f = folium.Figure(width=1000, height=1000)
m = folium.Map(location=[39, -17],
    zoom_start=5.5, min_zoom = 4).add_to(f)
mk = MarkerCluster().add_to(m)

d = df

numlinhas = d.shape[0]

for i in range(numlinhas):
    text = '<b>Data: </b>' + d.iloc[i]['data'] + '<br>'+ '<b>Hora: </b>' + d.iloc[i]['hora'] + '<br>' + '<b>Coordenadas: </b>' + d.iloc[i]['coordenadas'] + '<br>' + '<b>Area: </b>' + str(d.iloc[i]['area']) + '<br>' + '<b>Comprimento: </b>' + str(d.iloc[i]['comprimento'] )
    popup = folium.Popup(text, min_width=200, max_width=100)
    lat = d.iloc[i]['lat']
    lon = d.iloc[i]['lon']
    folium.Marker([lat,lon], popup=popup).add_to(mk)


f
#%%

