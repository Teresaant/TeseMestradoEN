import numpy as np
from numpy import argmin
from netCDF4 import Dataset, num2date
from datetime import datetime,date,time, timedelta
from pandas import DataFrame 
import pandas as pd

data1 = Dataset('2021current.nc','r')
        
time1 = data1.variables['time'][:].data # saber de todas as datas do respetivo ano (cada ficheiro 1 ano)

units1 = data1.variables['time'].units

time_modif1 = num2date(time1,units = units1,calendar = 'gregorian')

#Storing the lat and lon data of the netCDF file into variables
lat = data1.variables['latitude'][:]
lon = data1.variables['longitude'][:]


#df2017 = pd.read_csv("dados-2017.csv")
#df2018 = pd.read_csv("dados-2018.csv")
#df2019 = pd.read_csv("dados-2019.csv")
#df2020 = pd.read_csv("dados-2020.csv")
df2021 = pd.read_csv("dados-2021.csv")

lat_bd = []
lon_bd = []

for d in [df2021]:
    print(d)
    coords = d["coordenadas"].tolist()
    for c in coords:
        clat = c.split()[0]
        lat_d = int(clat[0:2])
        lat_m = int(clat[3:5])
        lat_s = int(clat[6:8])
        lat_bd.append(lat_d + lat_m/60 + lat_s/3600)

        clon = c.split()[1]
        lon_d = int(clon[0:3])
        lon_m = int(clon[4:6])
        lon_s = int(clon[7:9])
        lon_bd.append(-lon_d - lon_m/60 - lon_s/3600)
    
    d['lat'] = lat_bd
    d['lon'] = lon_bd



#lats_interesse=[]
#lons_interesse=[]
#for i,clat in enumerate(lat_bd):
    #clon = lon_bd[i]

    #if clat <= max(lat) and clat >= min(lat) and clon <=max(lon) and clon >=min(lon):
        #lats_interesse.append(clat)
        #lons_interesse.append(clon)




# Acrescenta a cada data frame as colunas latitude e longitude
#for d in [df2017]:
   # d["lat"] = [row["coordenadas"].split()[0] for i, row in d.iterrows()]
   # d["lon"] = [row["coordenadas"].split()[0] for i, row in d.iterrows()]

# Junta os dados dos vários anos
df = pd.concat([df2021])

#Heatmaps só funcionam com listas de listas, por isso devemos converter as data frames
#heat_df = df[['lat', 'lon','area']]
#heat_data = heat_df.values.tolist()

#print(heat_data)

date1 = []
for i in range(len(time_modif1)):# mudar para datetime
        b = time_modif1[i]
        reg = datetime(b.year, b.month, b.day, b.hour)
        date1.append(reg)

date_df = pd.to_datetime(df.data)

uo_d = []
vo_d = []

for i in range(len(df)):
    lat_d = lat_bd[i]
    lon_d = lon_bd[i]
    day = date_df.iloc[i]
    # hour = int(df.hora.iloc[i][0:2])
    t_d = date(day.year,day.month,day.day) #t_d = derrames date(day.year,day.month,day.day,hour)

    index_time = np.where(np.array(date1)==datetime.combine(t_d, time(12)))[0][0] #descobrir o local da nossa data

    nearest_lat = min(lat, key=lambda x:abs(x-lat_d))
    nearest_lon = min(lon, key=lambda x:abs(x-lon_d))

    index_lat = np.where(np.array(lat)==nearest_lat)[0][0]
    index_lon = np.where(np.array(lon)==nearest_lon)[0][0]

    uo_t_d = data1.variables['uo'][index_time,0,index_lat,index_lon] # east segue o lat
    vo_t_d = data1.variables['vo'][index_time,0,index_lat,index_lon] # north segue o lon

    uo_d.append(float(uo_t_d))
    vo_d.append(float(vo_t_d))

df['uo_current'] = uo_d
df['vo_current'] = vo_d

df2021.to_csv('2021_Current.csv')
print(df2021) 

# lat_d = lat_bd[i]
# lon_d = lon_bd[i]
# day = date_df.iloc[i]
# # hour = int(df.hora.iloc[i][0:2])
# t_d = date(day.year,day.month,day.day) #t_d = derrames date(day.year,day.month,day.day,hour)

# index_time = np.where(np.array(date1)==datetime.combine(t_d, time(12)))[0][0] #descobrir o local da nossa data

# nearest_lat = min(lat, key=lambda x:abs(x-lat_d))
# nearest_lon = min(lon, key=lambda x:abs(x-lon_d))

# index_lat = np.where(np.array(lat)==nearest_lat)[0][0]
# index_lon = np.where(np.array(lon)==nearest_lon)[0][0]

# uo_t_d = data1.variables['uo'][index_time,0,index_lat,index_lon] # east segue o lat
# vo_t_d = data1.variables['vo'][index_time,0,index_lat,index_lon] # north segue o lon


