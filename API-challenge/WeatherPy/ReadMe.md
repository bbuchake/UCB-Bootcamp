

```python
#Get dependencies
import requests
import json
from citipy import citipy
import numpy as np
import pandas as pd
from config import api_key
from config import url
import csv
import matplotlib.pyplot as plt


#Get a range of latitudes and longitudes
latitudes = np.linspace(-89, 89, num=1500)
print(len(latitudes)) #: There are 1500 latitudes

longitudes = np.random.uniform(low=-120, high=120, size=(1500,))
print(len(longitudes)) #: There are 1500 longitudes

#Combine latitudes and longitudes to locations
locations = np.column_stack((latitudes,longitudes))
print(len(locations)) #: There are 550 locations

cities_weather_df = pd.DataFrame(locations, columns=['Latitude', 'Longitude'])
cities_weather_df.head()
```

    1500
    1500
    1500





<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Latitude</th>
      <th>Longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-89.000000</td>
      <td>90.822793</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-88.881254</td>
      <td>95.436280</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-88.762508</td>
      <td>97.297490</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-88.643763</td>
      <td>57.823057</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-88.525017</td>
      <td>-64.211939</td>
    </tr>
  </tbody>
</table>
</div>




```python

#cities = []
for index, row in cities_weather_df.iterrows():
    city = citipy.nearest_city(row['Latitude'], row['Longitude'])
    cities_weather_df.set_value(index, 'City Name', city.city_name)

cities_weather_df.drop_duplicates(subset='City Name', keep="last", inplace=True)
cities_weather_df = cities_weather_df.reset_index(drop=True)
cities_weather_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>City Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-53.732488</td>
      <td>-72.006023</td>
      <td>punta arenas</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-53.138759</td>
      <td>39.168839</td>
      <td>east london</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-52.663776</td>
      <td>26.486130</td>
      <td>kruisfontein</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-51.832555</td>
      <td>-59.936929</td>
      <td>ushuaia</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-50.763843</td>
      <td>-45.481975</td>
      <td>mar del plata</td>
    </tr>
  </tbody>
</table>
</div>




```python

#Add other necessary columns to DataFrame
cities_weather_df['Temperature'] = ''
cities_weather_df['Humidity'] = ''
cities_weather_df['Cloudiness'] = ''
cities_weather_df['Windspeed'] = ''

cities_weather_df.head()

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>City Name</th>
      <th>Temperature</th>
      <th>Humidity</th>
      <th>Cloudiness</th>
      <th>Windspeed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-53.732488</td>
      <td>-72.006023</td>
      <td>punta arenas</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>-53.138759</td>
      <td>39.168839</td>
      <td>east london</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>-52.663776</td>
      <td>26.486130</td>
      <td>kruisfontein</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>-51.832555</td>
      <td>-59.936929</td>
      <td>ushuaia</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>-50.763843</td>
      <td>-45.481975</td>
      <td>mar del plata</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
#Time to call te Weather API

#Loop through cities and get weather data
#Print a log of all API calls
for index, row in cities_weather_df.iterrows():
    print("City Number: " + str(index) + " City Name: " + row['City Name'] + " Requested URL: " + url + "appid=" + api_key + "&units=Imperial&q=" + row['City Name'])
    response = requests.get(url + "appid=" + api_key + "&units=Imperial&q=" + row['City Name']).json()
    if response['cod'] == 200:
        cities_weather_df.set_value(index, 'Temperature', response['main']['temp'])
        cities_weather_df.set_value(index, 'Humidity', response['main']['humidity'])
        cities_weather_df.set_value(index, 'Cloudiness', response['clouds']['all'])
        cities_weather_df.set_value(index, 'Windspeed', response['wind']['speed'])
    else:
        continue
    

```

    City Number: 0 City Name: punta arenas Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=punta arenas
    City Number: 1 City Name: east london Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=east london
    City Number: 2 City Name: kruisfontein Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kruisfontein
    City Number: 3 City Name: ushuaia Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ushuaia
    City Number: 4 City Name: mar del plata Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mar del plata
    City Number: 5 City Name: rio gallegos Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rio gallegos
    City Number: 6 City Name: port alfred Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=port alfred
    City Number: 7 City Name: coihaique Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=coihaique
    City Number: 8 City Name: hermanus Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hermanus
    City Number: 9 City Name: port elizabeth Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=port elizabeth
    City Number: 10 City Name: cape town Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cape town
    City Number: 11 City Name: castro Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=castro
    City Number: 12 City Name: ancud Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ancud
    City Number: 13 City Name: chuy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=chuy
    City Number: 14 City Name: souillac Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=souillac
    City Number: 15 City Name: viedma Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=viedma
    City Number: 16 City Name: plettenberg bay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=plettenberg bay
    City Number: 17 City Name: bredasdorp Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bredasdorp
    City Number: 18 City Name: punta alta Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=punta alta
    City Number: 19 City Name: rocha Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rocha
    City Number: 20 City Name: san rafael Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=san rafael
    City Number: 21 City Name: santa rosa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=santa rosa
    City Number: 22 City Name: cidreira Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cidreira
    City Number: 23 City Name: albany Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=albany
    City Number: 24 City Name: san luis Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=san luis
    City Number: 25 City Name: saldanha Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saldanha
    City Number: 26 City Name: rio cuarto Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rio cuarto
    City Number: 27 City Name: venado tuerto Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=venado tuerto
    City Number: 28 City Name: laguna Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=laguna
    City Number: 29 City Name: san antonio Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=san antonio
    City Number: 30 City Name: paso de los toros Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=paso de los toros
    City Number: 31 City Name: cabildo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cabildo
    City Number: 32 City Name: umzimvubu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=umzimvubu
    City Number: 33 City Name: busselton Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=busselton
    City Number: 34 City Name: richards bay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=richards bay
    City Number: 35 City Name: ambovombe Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ambovombe
    City Number: 36 City Name: lebu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lebu
    City Number: 37 City Name: northam Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=northam
    City Number: 38 City Name: sao joao da barra Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sao joao da barra
    City Number: 39 City Name: beloha Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=beloha
    City Number: 40 City Name: arraial do cabo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=arraial do cabo
    City Number: 41 City Name: bloemfontein Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bloemfontein
    City Number: 42 City Name: santiago del estero Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=santiago del estero
    City Number: 43 City Name: geraldton Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=geraldton
    City Number: 44 City Name: oranjemund Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=oranjemund
    City Number: 45 City Name: taolanaro Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=taolanaro
    City Number: 46 City Name: curitibanos Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=curitibanos
    City Number: 47 City Name: armacao dos buzios Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=armacao dos buzios
    City Number: 48 City Name: mahebourg Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mahebourg
    City Number: 49 City Name: vila velha Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=vila velha
    City Number: 50 City Name: klerksdorp Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=klerksdorp
    City Number: 51 City Name: coquimbo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=coquimbo
    City Number: 52 City Name: tsihombe Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tsihombe
    City Number: 53 City Name: saint-joseph Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint-joseph
    City Number: 54 City Name: luderitz Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=luderitz
    City Number: 55 City Name: walvis bay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=walvis bay
    City Number: 56 City Name: corbelia Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=corbelia
    City Number: 57 City Name: taltal Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=taltal
    City Number: 58 City Name: chokwe Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=chokwe
    City Number: 59 City Name: jujuy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=jujuy
    City Number: 60 City Name: caravelas Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=caravelas
    City Number: 61 City Name: saint-philippe Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint-philippe
    City Number: 62 City Name: pisco Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pisco
    City Number: 63 City Name: rehoboth Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rehoboth
    City Number: 64 City Name: filadelfia Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=filadelfia
    City Number: 65 City Name: antofagasta Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=antofagasta
    City Number: 66 City Name: saint-leu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint-leu
    City Number: 67 City Name: bambous virieux Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bambous virieux
    City Number: 68 City Name: inhambane Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=inhambane
    City Number: 69 City Name: chipinge Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=chipinge
    City Number: 70 City Name: toliary Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=toliary
    City Number: 71 City Name: mananjary Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mananjary
    City Number: 72 City Name: henties bay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=henties bay
    City Number: 73 City Name: carnarvon Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=carnarvon
    City Number: 74 City Name: quelimane Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=quelimane
    City Number: 75 City Name: beira Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=beira
    City Number: 76 City Name: camana Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=camana
    City Number: 77 City Name: nokaneng Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nokaneng
    City Number: 78 City Name: linhares Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=linhares
    City Number: 79 City Name: chimoio Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=chimoio
    City Number: 80 City Name: grand river south east Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=grand river south east
    City Number: 81 City Name: andevoranto Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=andevoranto
    City Number: 82 City Name: karratha Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=karratha
    City Number: 83 City Name: hualmay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hualmay
    City Number: 84 City Name: governador valadares Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=governador valadares
    City Number: 85 City Name: mocuba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mocuba
    City Number: 86 City Name: namibe Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=namibe
    City Number: 87 City Name: port hedland Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=port hedland
    City Number: 88 City Name: angoche Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=angoche
    City Number: 89 City Name: marcona Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=marcona
    City Number: 90 City Name: arequipa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=arequipa
    City Number: 91 City Name: siavonga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=siavonga
    City Number: 92 City Name: huarmey Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=huarmey
    City Number: 93 City Name: quatre cocos Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=quatre cocos
    City Number: 94 City Name: bambanglipuro Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bambanglipuro
    City Number: 95 City Name: maceio Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=maceio
    City Number: 96 City Name: buritis Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=buritis
    City Number: 97 City Name: palabuhanratu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=palabuhanratu
    City Number: 98 City Name: guanay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=guanay
    City Number: 99 City Name: niquelandia Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=niquelandia
    City Number: 100 City Name: nobres Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nobres
    City Number: 101 City Name: jamestown Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=jamestown
    City Number: 102 City Name: palpa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=palpa
    City Number: 103 City Name: waingapu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=waingapu
    City Number: 104 City Name: cap malheureux Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cap malheureux
    City Number: 105 City Name: grand gaube Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=grand gaube
    City Number: 106 City Name: porangatu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=porangatu
    City Number: 107 City Name: cuamba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cuamba
    City Number: 108 City Name: macusani Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=macusani
    City Number: 109 City Name: diamantino Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=diamantino
    City Number: 110 City Name: chilca Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=chilca
    City Number: 111 City Name: srandakan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=srandakan
    City Number: 112 City Name: bengkulu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bengkulu
    City Number: 113 City Name: puerto maldonado Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=puerto maldonado
    City Number: 114 City Name: iberia Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=iberia
    City Number: 115 City Name: rikitea Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rikitea
    City Number: 116 City Name: sambava Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sambava
    City Number: 117 City Name: satipo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=satipo
    City Number: 118 City Name: dianopolis Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dianopolis
    City Number: 119 City Name: kibala Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kibala
    City Number: 120 City Name: koungou Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=koungou
    City Number: 121 City Name: karonga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=karonga
    City Number: 122 City Name: ambilobe Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ambilobe
    City Number: 123 City Name: olinda Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=olinda
    City Number: 124 City Name: malanje Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=malanje
    City Number: 125 City Name: aripuana Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aripuana
    City Number: 126 City Name: canto do buriti Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=canto do buriti
    City Number: 127 City Name: lucapa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lucapa
    City Number: 128 City Name: pimentel Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pimentel
    City Number: 129 City Name: kisanga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kisanga
    City Number: 130 City Name: kilindoni Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kilindoni
    City Number: 131 City Name: bulakamba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bulakamba
    City Number: 132 City Name: pitimbu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pitimbu
    City Number: 133 City Name: sao felix do xingu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sao felix do xingu
    City Number: 134 City Name: kasongo-lunda Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kasongo-lunda
    City Number: 135 City Name: parambu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=parambu
    City Number: 136 City Name: mgandu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mgandu
    City Number: 137 City Name: pangani Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pangani
    City Number: 138 City Name: kongolo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kongolo
    City Number: 139 City Name: cabedelo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cabedelo
    City Number: 140 City Name: atuona Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=atuona
    City Number: 141 City Name: chake chake Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=chake chake
    City Number: 142 City Name: mlonggo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mlonggo
    City Number: 143 City Name: codajas Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=codajas
    City Number: 144 City Name: talara Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=talara
    City Number: 145 City Name: mayumba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mayumba
    City Number: 146 City Name: tabou Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tabou
    City Number: 147 City Name: mangai Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mangai
    City Number: 148 City Name: kinkala Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kinkala
    City Number: 149 City Name: anori Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=anori
    City Number: 150 City Name: padang Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=padang
    City Number: 151 City Name: natal Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=natal
    City Number: 152 City Name: inongo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=inongo
    City Number: 153 City Name: iquitos Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=iquitos
    City Number: 154 City Name: porto de moz Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=porto de moz
    City Number: 155 City Name: acarau Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=acarau
    City Number: 156 City Name: matara Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=matara
    City Number: 157 City Name: hithadhoo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hithadhoo
    City Number: 158 City Name: fougamou Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=fougamou
    City Number: 159 City Name: pangkalanbuun Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pangkalanbuun
    City Number: 160 City Name: quevedo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=quevedo
    City Number: 161 City Name: kalangala Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kalangala
    City Number: 162 City Name: okandja Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=okandja
    City Number: 163 City Name: port-gentil Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=port-gentil
    City Number: 164 City Name: sao gabriel da cachoeira Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sao gabriel da cachoeira
    City Number: 165 City Name: miraflores Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=miraflores
    City Number: 166 City Name: sri aman Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sri aman
    City Number: 167 City Name: thinadhoo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=thinadhoo
    City Number: 168 City Name: georgetown Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=georgetown
    City Number: 169 City Name: santa isabel do rio negro Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=santa isabel do rio negro
    City Number: 170 City Name: sibolga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sibolga
    City Number: 171 City Name: mogadishu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mogadishu
    City Number: 172 City Name: harper Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=harper
    City Number: 173 City Name: grand-santi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=grand-santi
    City Number: 174 City Name: amudat Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=amudat
    City Number: 175 City Name: victoria Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=victoria
    City Number: 176 City Name: touros Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=touros
    City Number: 177 City Name: lodwar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lodwar
    City Number: 178 City Name: jawhar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=jawhar
    City Number: 179 City Name: aquiraz Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aquiraz
    City Number: 180 City Name: isiro Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=isiro
    City Number: 181 City Name: kudahuvadhoo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kudahuvadhoo
    City Number: 182 City Name: hambantota Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hambantota
    City Number: 183 City Name: puerto ayora Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=puerto ayora
    City Number: 184 City Name: meulaboh Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=meulaboh
    City Number: 185 City Name: san cristobal Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=san cristobal
    City Number: 186 City Name: salinopolis Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=salinopolis
    City Number: 187 City Name: xuddur Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=xuddur
    City Number: 188 City Name: warri Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=warri
    City Number: 189 City Name: pemangkat Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pemangkat
    City Number: 190 City Name: inirida Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=inirida
    City Number: 191 City Name: cotonou Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cotonou
    City Number: 192 City Name: kerteh Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kerteh
    City Number: 193 City Name: boa vista Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=boa vista
    City Number: 194 City Name: robertsport Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=robertsport
    City Number: 195 City Name: lazaro cardenas Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lazaro cardenas
    City Number: 196 City Name: saint-georges Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint-georges
    City Number: 197 City Name: dilla Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dilla
    City Number: 198 City Name: obuasi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=obuasi
    City Number: 199 City Name: mutis Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mutis
    City Number: 200 City Name: yala Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yala
    City Number: 201 City Name: tsevie Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tsevie
    City Number: 202 City Name: ugoofaaru Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ugoofaaru
    City Number: 203 City Name: la palma Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=la palma
    City Number: 204 City Name: kulhudhuffushi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kulhudhuffushi
    City Number: 205 City Name: arauca Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=arauca
    City Number: 206 City Name: cagayan de tawi-tawi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cagayan de tawi-tawi
    City Number: 207 City Name: bac lieu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bac lieu
    City Number: 208 City Name: tumpat Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tumpat
    City Number: 209 City Name: itarema Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=itarema
    City Number: 210 City Name: san jeronimo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=san jeronimo
    City Number: 211 City Name: sai buri Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sai buri
    City Number: 212 City Name: atakpame Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=atakpame
    City Number: 213 City Name: totness Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=totness
    City Number: 214 City Name: dhidhdhoo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dhidhdhoo
    City Number: 215 City Name: sabang Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sabang
    City Number: 216 City Name: eyl Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=eyl
    City Number: 217 City Name: bedele Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bedele
    City Number: 218 City Name: cayenne Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cayenne
    City Number: 219 City Name: sao filipe Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sao filipe
    City Number: 220 City Name: buenavista Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=buenavista
    City Number: 221 City Name: bubaque Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bubaque
    City Number: 222 City Name: ailigandi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ailigandi
    City Number: 223 City Name: bandarbeyla Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bandarbeyla
    City Number: 224 City Name: deder Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=deder
    City Number: 225 City Name: ranong Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ranong
    City Number: 226 City Name: barcelona Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=barcelona
    City Number: 227 City Name: ixtapa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ixtapa
    City Number: 228 City Name: ko samui Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ko samui
    City Number: 229 City Name: duku Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=duku
    City Number: 230 City Name: boke Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=boke
    City Number: 231 City Name: am timan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=am timan
    City Number: 232 City Name: kaduqli Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kaduqli
    City Number: 233 City Name: marabba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=marabba
    City Number: 234 City Name: san patricio Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=san patricio
    City Number: 235 City Name: puerto escondido Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=puerto escondido
    City Number: 236 City Name: grenville Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=grenville
    City Number: 237 City Name: juigalpa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=juigalpa
    City Number: 238 City Name: madras Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=madras
    City Number: 239 City Name: mergui Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mergui
    City Number: 240 City Name: massaguet Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=massaguet
    City Number: 241 City Name: san jose Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=san jose
    City Number: 242 City Name: kattivakkam Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kattivakkam
    City Number: 243 City Name: kavaratti Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kavaratti
    City Number: 244 City Name: tuy hoa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tuy hoa
    City Number: 245 City Name: sinjah Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sinjah
    City Number: 246 City Name: buluang Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=buluang
    City Number: 247 City Name: gummidipundi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=gummidipundi
    City Number: 248 City Name: qui nhon Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=qui nhon
    City Number: 249 City Name: tirthahalli Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tirthahalli
    City Number: 250 City Name: pochutla Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pochutla
    City Number: 251 City Name: champerico Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=champerico
    City Number: 252 City Name: bereda Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bereda
    City Number: 253 City Name: port blair Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=port blair
    City Number: 254 City Name: palauig Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=palauig
    City Number: 255 City Name: dogondoutchi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dogondoutchi
    City Number: 256 City Name: tanout Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tanout
    City Number: 257 City Name: nioro Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nioro
    City Number: 258 City Name: nueva armenia Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nueva armenia
    City Number: 259 City Name: tecpan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tecpan
    City Number: 260 City Name: umm kaddadah Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=umm kaddadah
    City Number: 261 City Name: sokolo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sokolo
    City Number: 262 City Name: louga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=louga
    City Number: 263 City Name: porto novo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=porto novo
    City Number: 264 City Name: biltine Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=biltine
    City Number: 265 City Name: pyapon Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pyapon
    City Number: 266 City Name: ratnagiri Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ratnagiri
    City Number: 267 City Name: kutum Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kutum
    City Number: 268 City Name: bathsheba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bathsheba
    City Number: 269 City Name: morant bay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=morant bay
    City Number: 270 City Name: wanning Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=wanning
    City Number: 271 City Name: richard toll Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=richard toll
    City Number: 272 City Name: srivardhan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=srivardhan
    City Number: 273 City Name: najran Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=najran
    City Number: 274 City Name: sawang daen din Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sawang daen din
    City Number: 275 City Name: sinnamary Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sinnamary
    City Number: 276 City Name: manzanillo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=manzanillo
    City Number: 277 City Name: the valley Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=the valley
    City Number: 278 City Name: aguililla Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aguililla
    City Number: 279 City Name: kidal Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kidal
    City Number: 280 City Name: akyab Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=akyab
    City Number: 281 City Name: bacalar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bacalar
    City Number: 282 City Name: higuey Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=higuey
    City Number: 283 City Name: jeremie Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=jeremie
    City Number: 284 City Name: road town Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=road town
    City Number: 285 City Name: salalah Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=salalah
    City Number: 286 City Name: sur Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sur
    City Number: 287 City Name: bucerias Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bucerias
    City Number: 288 City Name: abu samrah Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=abu samrah
    City Number: 289 City Name: yamethin Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yamethin
    City Number: 290 City Name: harindanga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=harindanga
    City Number: 291 City Name: caucel Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=caucel
    City Number: 292 City Name: cabo san lucas Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cabo san lucas
    City Number: 293 City Name: cockburn town Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cockburn town
    City Number: 294 City Name: ranavav Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ranavav
    City Number: 295 City Name: raigarh Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=raigarh
    City Number: 296 City Name: mazatlan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mazatlan
    City Number: 297 City Name: mecca Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mecca
    City Number: 298 City Name: bilma Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bilma
    City Number: 299 City Name: lalmohan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lalmohan
    City Number: 300 City Name: birmitrapur Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=birmitrapur
    City Number: 301 City Name: gat Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=gat
    City Number: 302 City Name: faya Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=faya
    City Number: 303 City Name: nandu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nandu
    City Number: 304 City Name: nouadhibou Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nouadhibou
    City Number: 305 City Name: nuevo progreso Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nuevo progreso
    City Number: 306 City Name: huaicheng Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=huaicheng
    City Number: 307 City Name: binzhou Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=binzhou
    City Number: 308 City Name: rapar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rapar
    City Number: 309 City Name: la paz Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=la paz
    City Number: 310 City Name: key west Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=key west
    City Number: 311 City Name: aguimes Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aguimes
    City Number: 312 City Name: manasa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=manasa
    City Number: 313 City Name: hailakandi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hailakandi
    City Number: 314 City Name: constitucion Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=constitucion
    City Number: 315 City Name: khajuraho Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=khajuraho
    City Number: 316 City Name: alice town Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=alice town
    City Number: 317 City Name: riyadh Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=riyadh
    City Number: 318 City Name: ponta do sol Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ponta do sol
    City Number: 319 City Name: yongan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yongan
    City Number: 320 City Name: houma Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=houma
    City Number: 321 City Name: ahome Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ahome
    City Number: 322 City Name: asyut Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=asyut
    City Number: 323 City Name: codrington Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=codrington
    City Number: 324 City Name: tlahualilo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tlahualilo
    City Number: 325 City Name: jalu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=jalu
    City Number: 326 City Name: guerrero negro Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=guerrero negro
    City Number: 327 City Name: panzhihua Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=panzhihua
    City Number: 328 City Name: tundla Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tundla
    City Number: 329 City Name: kingsville Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kingsville
    City Number: 330 City Name: dalbandin Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dalbandin
    City Number: 331 City Name: xichang Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=xichang
    City Number: 332 City Name: santa rosalia Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=santa rosalia
    City Number: 333 City Name: galveston Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=galveston
    City Number: 334 City Name: marsa matruh Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=marsa matruh
    City Number: 335 City Name: quzhou Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=quzhou
    City Number: 336 City Name: adrar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=adrar
    City Number: 337 City Name: warqla Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=warqla
    City Number: 338 City Name: doha Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=doha
    City Number: 339 City Name: tacoronte Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tacoronte
    City Number: 340 City Name: los llanos de aridane Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=los llanos de aridane
    City Number: 341 City Name: hamilton Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hamilton
    City Number: 342 City Name: lanxi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lanxi
    City Number: 343 City Name: jalalabad Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=jalalabad
    City Number: 344 City Name: sultanpur Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sultanpur
    City Number: 345 City Name: tiznit Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tiznit
    City Number: 346 City Name: mastung Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mastung
    City Number: 347 City Name: chizhou Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=chizhou
    City Number: 348 City Name: nalut Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nalut
    City Number: 349 City Name: qianjiang Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=qianjiang
    City Number: 350 City Name: sakakah Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sakakah
    City Number: 351 City Name: huayang Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=huayang
    City Number: 352 City Name: saint simons Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint simons
    City Number: 353 City Name: san angelo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=san angelo
    City Number: 354 City Name: yaan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yaan
    City Number: 355 City Name: port said Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=port said
    City Number: 356 City Name: zhob Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=zhob
    City Number: 357 City Name: taft Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=taft
    City Number: 358 City Name: corsicana Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=corsicana
    City Number: 359 City Name: baoning Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=baoning
    City Number: 360 City Name: wilmington Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=wilmington
    City Number: 361 City Name: selma Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=selma
    City Number: 362 City Name: ravar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ravar
    City Number: 363 City Name: tabas Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tabas
    City Number: 364 City Name: tezu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tezu
    City Number: 365 City Name: along Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=along
    City Number: 366 City Name: daultala Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=daultala
    City Number: 367 City Name: asfi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=asfi
    City Number: 368 City Name: birjand Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=birjand
    City Number: 369 City Name: koutsouras Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=koutsouras
    City Number: 370 City Name: fountain hills Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=fountain hills
    City Number: 371 City Name: uruzgan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=uruzgan
    City Number: 372 City Name: aflu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aflu
    City Number: 373 City Name: ardakan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ardakan
    City Number: 374 City Name: lasa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lasa
    City Number: 375 City Name: roswell Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=roswell
    City Number: 376 City Name: ponta delgada Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ponta delgada
    City Number: 377 City Name: ada Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ada
    City Number: 378 City Name: pagman Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pagman
    City Number: 379 City Name: abu kamal Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=abu kamal
    City Number: 380 City Name: waynesville Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=waynesville
    City Number: 381 City Name: saint george Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint george
    City Number: 382 City Name: grants Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=grants
    City Number: 383 City Name: virginia beach Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=virginia beach
    City Number: 384 City Name: semnan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=semnan
    City Number: 385 City Name: pingliang Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pingliang
    City Number: 386 City Name: constantine Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=constantine
    City Number: 387 City Name: wahran Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=wahran
    City Number: 388 City Name: xining Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=xining
    City Number: 389 City Name: almeria Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=almeria
    City Number: 390 City Name: melito di porto salvo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=melito di porto salvo
    City Number: 391 City Name: gilgit Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=gilgit
    City Number: 392 City Name: rudsar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rudsar
    City Number: 393 City Name: brigantine Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=brigantine
    City Number: 394 City Name: atlantic city Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=atlantic city
    City Number: 395 City Name: camacha Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=camacha
    City Number: 396 City Name: hunza Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hunza
    City Number: 397 City Name: aksu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aksu
    City Number: 398 City Name: aliartos Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aliartos
    City Number: 399 City Name: luancheng Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=luancheng
    City Number: 400 City Name: azuaga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=azuaga
    City Number: 401 City Name: mahon Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mahon
    City Number: 402 City Name: nantucket Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nantucket
    City Number: 403 City Name: koson Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=koson
    City Number: 404 City Name: saint-pierre Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint-pierre
    City Number: 405 City Name: daimiel Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=daimiel
    City Number: 406 City Name: garden city Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=garden city
    City Number: 407 City Name: liverpool Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=liverpool
    City Number: 408 City Name: korla Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=korla
    City Number: 409 City Name: imisli Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=imisli
    City Number: 410 City Name: springfield Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=springfield
    City Number: 411 City Name: sorrento Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sorrento
    City Number: 412 City Name: poliyiros Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=poliyiros
    City Number: 413 City Name: sterling Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sterling
    City Number: 414 City Name: iskilip Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=iskilip
    City Number: 415 City Name: resen Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=resen
    City Number: 416 City Name: haibowan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=haibowan
    City Number: 417 City Name: peniche Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=peniche
    City Number: 418 City Name: rock springs Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rock springs
    City Number: 419 City Name: orbetello Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=orbetello
    City Number: 420 City Name: bansko Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bansko
    City Number: 421 City Name: ribeira grande Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ribeira grande
    City Number: 422 City Name: vila franca do campo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=vila franca do campo
    City Number: 423 City Name: ardesen Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ardesen
    City Number: 424 City Name: hovd Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hovd
    City Number: 425 City Name: penne Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=penne
    City Number: 426 City Name: oytal Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=oytal
    City Number: 427 City Name: portoferraio Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=portoferraio
    City Number: 428 City Name: chifeng Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=chifeng
    City Number: 429 City Name: muros Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=muros
    City Number: 430 City Name: yumen Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yumen
    City Number: 431 City Name: batavia Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=batavia
    City Number: 432 City Name: hami Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hami
    City Number: 433 City Name: beyneu Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=beyneu
    City Number: 434 City Name: muret Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=muret
    City Number: 435 City Name: mandalgovi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mandalgovi
    City Number: 436 City Name: lander Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lander
    City Number: 437 City Name: changji Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=changji
    City Number: 438 City Name: randolph Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=randolph
    City Number: 439 City Name: rodez Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rodez
    City Number: 440 City Name: pesaro Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pesaro
    City Number: 441 City Name: littleton Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=littleton
    City Number: 442 City Name: gijon Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=gijon
    City Number: 443 City Name: sarlat-la-caneda Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sarlat-la-caneda
    City Number: 444 City Name: aviles Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aviles
    City Number: 445 City Name: louisbourg Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=louisbourg
    City Number: 446 City Name: aberdeen Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aberdeen
    City Number: 447 City Name: rabo de peixe Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rabo de peixe
    City Number: 448 City Name: bovolone Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bovolone
    City Number: 449 City Name: zhanatas Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=zhanatas
    City Number: 450 City Name: marinette Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=marinette
    City Number: 451 City Name: vercheres Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=vercheres
    City Number: 452 City Name: rence Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rence
    City Number: 453 City Name: hermiston Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hermiston
    City Number: 454 City Name: dickinson Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dickinson
    City Number: 455 City Name: brainerd Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=brainerd
    City Number: 456 City Name: zhezkazgan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=zhezkazgan
    City Number: 457 City Name: baijiantan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=baijiantan
    City Number: 458 City Name: ulaangom Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ulaangom
    City Number: 459 City Name: balykshi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=balykshi
    City Number: 460 City Name: ketchenery Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ketchenery
    City Number: 461 City Name: la chaux-de-fonds Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=la chaux-de-fonds
    City Number: 462 City Name: campbellton Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=campbellton
    City Number: 463 City Name: burgeo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=burgeo
    City Number: 464 City Name: gulshat Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=gulshat
    City Number: 465 City Name: tambovka Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tambovka
    City Number: 466 City Name: zaysan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=zaysan
    City Number: 467 City Name: altay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=altay
    City Number: 468 City Name: mezhova Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mezhova
    City Number: 469 City Name: penzance Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=penzance
    City Number: 470 City Name: bulgan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bulgan
    City Number: 471 City Name: mitoc Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mitoc
    City Number: 472 City Name: mynay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mynay
    City Number: 473 City Name: inderborskiy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=inderborskiy
    City Number: 474 City Name: cap-chat Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cap-chat
    City Number: 475 City Name: shar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=shar
    City Number: 476 City Name: kyra Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kyra
    City Number: 477 City Name: vizovice Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=vizovice
    City Number: 478 City Name: svetlyy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=svetlyy
    City Number: 479 City Name: ozinki Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ozinki
    City Number: 480 City Name: torbay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=torbay
    City Number: 481 City Name: kenora Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kenora
    City Number: 482 City Name: kosh-agach Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kosh-agach
    City Number: 483 City Name: lagoa Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=lagoa
    City Number: 484 City Name: thunder bay Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=thunder bay
    City Number: 485 City Name: krasnyy chikoy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=krasnyy chikoy
    City Number: 486 City Name: matagami Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=matagami
    City Number: 487 City Name: pervoye maya Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pervoye maya
    City Number: 488 City Name: bassano Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bassano
    City Number: 489 City Name: saint-ambroise Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint-ambroise
    City Number: 490 City Name: kindersley Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kindersley
    City Number: 491 City Name: swidnik Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=swidnik
    City Number: 492 City Name: sittingbourne Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sittingbourne
    City Number: 493 City Name: ilek Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ilek
    City Number: 494 City Name: wolfen Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=wolfen
    City Number: 495 City Name: gorno-altaysk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=gorno-altaysk
    City Number: 496 City Name: grindavik Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=grindavik
    City Number: 497 City Name: sotnikovo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sotnikovo
    City Number: 498 City Name: sretensk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sretensk
    City Number: 499 City Name: sosnovo-ozerskoye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sosnovo-ozerskoye
    City Number: 500 City Name: malaya serdoba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=malaya serdoba
    City Number: 501 City Name: tralee Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tralee
    City Number: 502 City Name: ivanava Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ivanava
    City Number: 503 City Name: haverfordwest Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=haverfordwest
    City Number: 504 City Name: toora-khem Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=toora-khem
    City Number: 505 City Name: ramasukha Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ramasukha
    City Number: 506 City Name: belinskiy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=belinskiy
    City Number: 507 City Name: hrodna Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hrodna
    City Number: 508 City Name: nizhneudinsk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nizhneudinsk
    City Number: 509 City Name: fershampenuaz Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=fershampenuaz
    City Number: 510 City Name: bonavista Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bonavista
    City Number: 511 City Name: polovinnoye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=polovinnoye
    City Number: 512 City Name: kozelsk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kozelsk
    City Number: 513 City Name: tulun Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tulun
    City Number: 514 City Name: dobre miasto Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dobre miasto
    City Number: 515 City Name: ribnitz-damgarten Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ribnitz-damgarten
    City Number: 516 City Name: dingle Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dingle
    City Number: 517 City Name: zverinogolovskoye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=zverinogolovskoye
    City Number: 518 City Name: kachug Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kachug
    City Number: 519 City Name: sept-iles Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sept-iles
    City Number: 520 City Name: shestakovo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=shestakovo
    City Number: 521 City Name: nordby Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nordby
    City Number: 522 City Name: zelenogradsk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=zelenogradsk
    City Number: 523 City Name: bolotnoye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bolotnoye
    City Number: 524 City Name: havre-saint-pierre Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=havre-saint-pierre
    City Number: 525 City Name: belyy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=belyy
    City Number: 526 City Name: den helder Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=den helder
    City Number: 527 City Name: krasnokholmskiy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=krasnokholmskiy
    City Number: 528 City Name: blyth Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=blyth
    City Number: 529 City Name: morki Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=morki
    City Number: 530 City Name: surok Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=surok
    City Number: 531 City Name: moryakovskiy zaton Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=moryakovskiy zaton
    City Number: 532 City Name: westport Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=westport
    City Number: 533 City Name: peace river Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=peace river
    City Number: 534 City Name: sukhobezvodnoye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sukhobezvodnoye
    City Number: 535 City Name: cesvaine Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=cesvaine
    City Number: 536 City Name: krasnyy yar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=krasnyy yar
    City Number: 537 City Name: aleksandrovskoye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aleksandrovskoye
    City Number: 538 City Name: pervomayskoye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pervomayskoye
    City Number: 539 City Name: moose factory Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=moose factory
    City Number: 540 City Name: peterhead Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=peterhead
    City Number: 541 City Name: ballina Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ballina
    City Number: 542 City Name: saint-augustin Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saint-augustin
    City Number: 543 City Name: danilov Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=danilov
    City Number: 544 City Name: turtas Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=turtas
    City Number: 545 City Name: grand centre Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=grand centre
    City Number: 546 City Name: la ronge Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=la ronge
    City Number: 547 City Name: gdov Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=gdov
    City Number: 548 City Name: katrineholm Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=katrineholm
    City Number: 549 City Name: maarianhamina Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=maarianhamina
    City Number: 550 City Name: usolye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=usolye
    City Number: 551 City Name: yefimovskiy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yefimovskiy
    City Number: 552 City Name: nanortalik Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nanortalik
    City Number: 553 City Name: novaya ladoga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=novaya ladoga
    City Number: 554 City Name: helsinki Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=helsinki
    City Number: 555 City Name: malinovskiy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=malinovskiy
    City Number: 556 City Name: yertsevo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yertsevo
    City Number: 557 City Name: stanghelle Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=stanghelle
    City Number: 558 City Name: hay river Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hay river
    City Number: 559 City Name: sandane Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sandane
    City Number: 560 City Name: nuuk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=nuuk
    City Number: 561 City Name: qaqortoq Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=qaqortoq
    City Number: 562 City Name: almaznyy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=almaznyy
    City Number: 563 City Name: flin flon Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=flin flon
    City Number: 564 City Name: novoagansk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=novoagansk
    City Number: 565 City Name: yarega Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yarega
    City Number: 566 City Name: turukhansk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=turukhansk
    City Number: 567 City Name: oktyabrskoye Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=oktyabrskoye
    City Number: 568 City Name: iisalmi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=iisalmi
    City Number: 569 City Name: teya Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=teya
    City Number: 570 City Name: sorvag Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sorvag
    City Number: 571 City Name: verkhnyaya inta Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=verkhnyaya inta
    City Number: 572 City Name: iqaluit Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=iqaluit
    City Number: 573 City Name: kristiansund Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kristiansund
    City Number: 574 City Name: koslan Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=koslan
    City Number: 575 City Name: olafsvik Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=olafsvik
    City Number: 576 City Name: gubkinskiy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=gubkinskiy
    City Number: 577 City Name: attawapiskat Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=attawapiskat
    City Number: 578 City Name: aykhal Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aykhal
    City Number: 579 City Name: ust-tsilma Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ust-tsilma
    City Number: 580 City Name: pangody Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pangody
    City Number: 581 City Name: rovaniemi Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=rovaniemi
    City Number: 582 City Name: urengoy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=urengoy
    City Number: 583 City Name: raudeberg Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=raudeberg
    City Number: 584 City Name: staryy nadym Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=staryy nadym
    City Number: 585 City Name: skagastrond Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=skagastrond
    City Number: 586 City Name: hofn Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=hofn
    City Number: 587 City Name: usinsk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=usinsk
    City Number: 588 City Name: umba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=umba
    City Number: 589 City Name: qasigiannguit Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=qasigiannguit
    City Number: 590 City Name: naryan-mar Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=naryan-mar
    City Number: 591 City Name: tura Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tura
    City Number: 592 City Name: sorland Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=sorland
    City Number: 593 City Name: kharp Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=kharp
    City Number: 594 City Name: aksarka Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=aksarka
    City Number: 595 City Name: zhigansk Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=zhigansk
    City Number: 596 City Name: dudinka Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dudinka
    City Number: 597 City Name: bolungarvik Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=bolungarvik
    City Number: 598 City Name: brae Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=brae
    City Number: 599 City Name: mezen Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mezen
    City Number: 600 City Name: polyarnyy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=polyarnyy
    City Number: 601 City Name: karaul Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=karaul
    City Number: 602 City Name: andenes Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=andenes
    City Number: 603 City Name: tazovskiy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tazovskiy
    City Number: 604 City Name: pangnirtung Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=pangnirtung
    City Number: 605 City Name: tromso Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tromso
    City Number: 606 City Name: stokmarknes Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=stokmarknes
    City Number: 607 City Name: clyde river Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=clyde river
    City Number: 608 City Name: yar-sale Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yar-sale
    City Number: 609 City Name: vardo Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=vardo
    City Number: 610 City Name: husavik Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=husavik
    City Number: 611 City Name: thompson Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=thompson
    City Number: 612 City Name: ostrovnoy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ostrovnoy
    City Number: 613 City Name: mehamn Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=mehamn
    City Number: 614 City Name: norman wells Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=norman wells
    City Number: 615 City Name: tasiilaq Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tasiilaq
    City Number: 616 City Name: klaksvik Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=klaksvik
    City Number: 617 City Name: ilulissat Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=ilulissat
    City Number: 618 City Name: talnakh Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=talnakh
    City Number: 619 City Name: illoqqortoormiut Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=illoqqortoormiut
    City Number: 620 City Name: khatanga Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=khatanga
    City Number: 621 City Name: tumannyy Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=tumannyy
    City Number: 622 City Name: barentsburg Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=barentsburg
    City Number: 623 City Name: yellowknife Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=yellowknife
    City Number: 624 City Name: narsaq Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=narsaq
    City Number: 625 City Name: saskylakh Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=saskylakh
    City Number: 626 City Name: amderma Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=amderma
    City Number: 627 City Name: belushya guba Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=belushya guba
    City Number: 628 City Name: dikson Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=dikson
    City Number: 629 City Name: longyearbyen Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=longyearbyen
    City Number: 630 City Name: upernavik Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=upernavik
    City Number: 631 City Name: qaanaaq Requested URL: http://api.openweathermap.org/data/2.5/weather?appid=3628d1179477d278e3da5e94fc2f1cad&units=Imperial&q=qaanaaq



```python
#Remove cities that were not found
filter = cities_weather_df['Temperature'] != ""
cities_weather_df = cities_weather_df[filter]
cities_weather_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>City Name</th>
      <th>Temperature</th>
      <th>Humidity</th>
      <th>Cloudiness</th>
      <th>Windspeed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-53.732488</td>
      <td>-72.006023</td>
      <td>punta arenas</td>
      <td>33.8</td>
      <td>74</td>
      <td>20</td>
      <td>6.93</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-53.138759</td>
      <td>39.168839</td>
      <td>east london</td>
      <td>64.4</td>
      <td>82</td>
      <td>40</td>
      <td>14.99</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-52.663776</td>
      <td>26.486130</td>
      <td>kruisfontein</td>
      <td>66.94</td>
      <td>91</td>
      <td>76</td>
      <td>18.03</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-51.832555</td>
      <td>-59.936929</td>
      <td>ushuaia</td>
      <td>35.6</td>
      <td>100</td>
      <td>75</td>
      <td>16.11</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-50.763843</td>
      <td>-45.481975</td>
      <td>mar del plata</td>
      <td>57.94</td>
      <td>57</td>
      <td>0</td>
      <td>24.07</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Save to csv
cities_weather_df.to_csv("Weather Data.csv")
```

Latitude vs Temperature Plot


```python
#Start scatter plotting
#Latitude vs Temperature
x_axis = cities_weather_df['Latitude']
data = cities_weather_df['Temperature']

plt.scatter(x_axis, data)
plt.title("City Latitude vs Max Temperature (03/18/2018)")
plt.xlabel("Latitude")
plt.ylabel("Temperature (F)")
plt.grid()
plt.savefig('temp_scatter.png')
plt.show()


```


![png](output_7_0.png)


Latitude vs Humidity Plot


```python
#Latitude vs Humidity
x_axis = cities_weather_df['Latitude']
data = cities_weather_df['Humidity']

plt.scatter(x_axis, data, color='r')
plt.title("City Latitude vs Humidity (03/18/2018)")
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.grid()
plt.savefig('humidity_scatter.png')
plt.show()
```


![png](output_9_0.png)


Latitude vs Cloudiness Plot


```python
#Latitude vs Cloudiness
x_axis = cities_weather_df['Latitude']
data = cities_weather_df['Cloudiness']

plt.scatter(x_axis, data, color='g')
plt.title("City Latitude vs Cloudiness (03/18/2018)")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.grid()
plt.savefig('cloudiness_scatter.png')
plt.show()
```


![png](output_11_0.png)


Latitude vs Windspeed Plot


```python
#Latitude vs Windspeed
x_axis = cities_weather_df['Latitude']
data = cities_weather_df['Windspeed']

plt.scatter(x_axis, data, color='y')
plt.title("City Latitude vs Windspeed (03/18/2018)")
plt.xlabel("Latitude")
plt.ylabel("Windspeed (mph)")
plt.grid()
plt.savefig('windspeed_scatter.png')
plt.show()
```


![png](output_13_0.png)

