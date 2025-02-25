from bs4 import BeautifulSoup
import pandas as pd

with open('data/pagina.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

filtered_div = soup.find_all("div", {"class": "row clubrow"})

tablas = filtered_div[2].find_all('table')

rows = soup.find_all('tr', {"class": "hidden-lg hidden-md white-stripe"})

dates = []
matches = []

for row in rows:
    date = row.find('div', {"class": "event-date"})
    if date:
        match_title = row.find('a', {"class": "btn-small-blue"}).get('title')
        dates.append(date.text.strip())
        matches.append(match_title.replace('Match report ',''))

df = pd.DataFrame({'date': dates, 'match': matches})
df['datetime_column'] = pd.to_datetime(df['date'], format='%d %b %H:%M')

df['identifier'] = (df['datetime_column'].dt.day.astype(str) + 
                    '-' + df['datetime_column'].dt.month.astype(str))

df=df[["identifier","match"]]
df=df.drop_duplicates()

df.to_csv("data/matches.csv")