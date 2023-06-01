import pandas as pd
import requests

# Ссылка на таблицу Google Sheets
url = 'https://docs.google.com/spreadsheets/d/18919E41_ZwY-9JECB8wGRc6iewUf5q1bSpna_q3YYU8/export?format=xlsx'

# Создаем запрос GET на URL-адрес
r = requests.get(url)

# Загружаем данные Excel в DataFrame с помощью функции read_excel() библиотеки pandas
df = pd.read_excel(r.content)

df.to_csv(path_or_buf='exapmle.csv')
print(df)

# url = 'https://docs.google.com/spreadsheets/d/18919E41_ZwY-9JECB8wGRc6iewUf5q1bSpna_q3YYU8/edit?usp=sharing'
