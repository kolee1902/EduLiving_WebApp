import pandas as pd
import requests
import io
import sys
sys.stdout.reconfigure(encoding='utf-8')


df_schools = pd.read_csv('schools.csv', encoding='utf-8')
df_schools = df_schools[["Khu vực", "Địa chỉ", "Tên đơn vị", "Công Lập", "Tư Thục", "Trường Chuyên?"]]
df_representative_schools = df_schools

df_real_estate = pd.read_csv('processed_mogi_hcm.csv', encoding='utf-8')
df_real_estate = df_real_estate[df_real_estate['Loại BĐS'] != 'Biệt thự']
df_real_estate = df_real_estate[(df_real_estate['Quận/Huyện'] == 'Quận 5') | (df_real_estate['Quận/Huyện'] == 'Thành phố Thủ Đức')]

df_real_estate1 = df_real_estate
df_real_estate1['Địa chỉ đầy đủ'] = df_real_estate1['Đường'] + ', ' + df_real_estate1['Phường/Xã'] + ', ' + df_real_estate1['Quận/Huyện'] + ', ' + df_real_estate1['Thành phố']
df_real_estate1 = df_real_estate1[["Quận/Huyện", 'Địa chỉ đầy đủ', 'Mã BĐS', "Tiêu đề", "Giá (tỷ)"]]

# Due to the large amount of data, limited tools and APIs. We will randomly select  real estates to calculate the distance to schools in the same area.
df_real_estates_filtered = df_real_estate1.groupby('Quận/Huyện').apply(lambda x: x.sample(n=100)).reset_index(drop=True)

df_final = pd.merge(df_representative_schools, df_real_estates_filtered, 
                    left_on='Khu vực', right_on='Quận/Huyện', how='inner')

df_final.to_csv('school - real estate.csv', index=False, encoding='utf-8-sig')