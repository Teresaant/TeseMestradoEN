import numpy as np 
from datetime import datetime, time, date, timedelta
import pandas as pd
from netCDF4 import Dataset, num2date

df2017 = pd.read_csv("dados-2017.csv")
#set_dez2020 = df2020.loc[260:405,] #se o ficheiro for muito grande e só der para ser por meses

lat_bd = []
lon_bd = []
#for d in [df2017, df2018, df2019, df2020, df2021]:
for d in [df2017]:
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

data1 = Dataset('2017_Wind_Eastward.nc')

time1 = data1.variables['time'][:]

units1 = data1.variables['time'].units

time_modif1 = num2date(time1.data, units = units1, calendar = 'gregorian') 

lat = data1.variables['lat'][:]
lon = data1.variables['lon'][:]

date1 = []
for i in range(len(time_modif1)): # mudar para datetime
    b = time_modif1[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date1.append(reg)

#date_df = pd.to_datetime(df.data, dayfirst=True)
date_df = pd.to_datetime(df2017.data, dayfirst=True)

eastward_wind_d = []
#northward_wind_d = []
index_int = []
lat_int = []
lon_int = []

for i in range(len(df2017)):
    lat_d = lat_bd[i]
    lon_d = lon_bd[i]
    day = date_df.iloc[i]
    #hour = time(int(df2021.hora.iloc[i][0:2]))
    t_d = date(day.year,day.month,day.day) #t_d = derrames date(day.year,day.month,day.day,hour)

    index_time = np.where(np.array(date1)==datetime.combine(t_d,time(0)))[0][0] #descobrir o local da nossa data

    nearest_lat = min(lat, key=lambda x:abs(x-lat_d))
    nearest_lon = min(lon, key=lambda x:abs(x-lon_d))

    index_lat = np.where(np.array(lat)==nearest_lat)[0][0]
    index_lon = np.where(np.array(lon)==nearest_lon)[0][0]

    east_wind_t_d = data1.variables['eastward_wind'][index_time, index_lat, index_lon]
    #north_wind_t_d = data1.variables['northward_wind'][index_time, index_lat, index_lon]

    eastward_wind_d.append(float(east_wind_t_d))
    #northward_wind_d.append(float(north_wind_t_d))
    index_int.append(index_time)
    lat_int.append(index_lat)
    lon_int.append(index_lon)


df2017['east_wind'] = eastward_wind_d
#df2017['north_wind'] = northward_wind_d

df2017.to_csv('2017_Wind_Eastward.csv')
print(df2017) 
