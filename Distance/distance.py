import pandas as pd
import requests
import io
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Use openstreetmap to get coordinates
def get_coordinates(address):
    url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'
    headers = {
        'User-Agent': 'YourAppName/1.0 (aibaygio123@gmail.com)'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200 and response.text:
        data = response.json()
        
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            print(f"No results for address: {address}")
            return None, None
    else:
        print("Error connecting to API or no results.")
        return None, None

# Calculate distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2

    R = 6371.0  # Radius of the Earth in kilometers
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

df_merged = pd.read_csv('school - real estate.csv', encoding='utf-8')
i = 0
distances = []

for index, row in df_merged.iterrows():
    lat1, lon1 = get_coordinates(row['Địa chỉ'])
    lat2, lon2 = get_coordinates(row['Địa chỉ đầy đủ'])
    i += 1

    if lat1 is not None and lat2 is not None:
        distance = haversine(lat1, lon1, lat2, lon2)
        distances.append(distance)
        print(distance)
    else:
        distances.append(None) 
    print(i)

df_merged['Khoảng cách'] = distances

df_merged.to_csv('dis_data.csv', index=False, encoding='utf-8-sig')