from bs4 import BeautifulSoup
import pandas as pd

with open('data/pagina.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

filtered_div = soup.find_all("div", {"class": "row clubrow"})

tablas = filtered_div[2].find_all('table')
data = []

for table in tablas:
    for row in table.find_all('tr', {"class": "hidden-sm hidden-xs"})[1:]:  
        cols = row.find_all('td')
        if len(cols) >= 5:
            date = cols[0].text.strip()
            mins = cols[2].text.strip()
            event = cols[3].text.strip()
            score = cols[4].text.strip()
            team = cols[5].text.strip()
            competition = cols[6].text.strip()
            data.append([date, mins, event, score, team, competition])

columns = ['date', 'mins', 'event', 'score', 'team', 'competition']
dataframe = pd.DataFrame(data, columns=columns)

dataframe['datetime_column'] = pd.to_datetime(dataframe['date'], format='%d %b %H:%M')

dataframe['identifier'] = (dataframe['datetime_column'].dt.day.astype(str) + 
                    '-' + dataframe['datetime_column'].dt.month.astype(str))

dataframe.to_csv("data/harborough.csv")