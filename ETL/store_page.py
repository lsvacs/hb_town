import requests

url = 'https://southern-football-league.co.uk/team/Harborough/2385/2024/2025/P'

response = requests.get(url)

if response.status_code == 200:
    with open('data/pagina.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
else:
    print(f'Error al realizar la solicitud: {response.status_code}')