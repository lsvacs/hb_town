
## ¿Como se construyo la mini demo?

Se realizá uan extracción de datos directamente de la página https://southern-football-league.co.uk/team/Harborough/2385/2024/2025/P y se almacena la información en un archivo html para evitar hacer peticiones recurrentes a la fuente.

Se le da una estructura a la información, generando un csv que separe la información de los partidos, los eventos, los minutos, los jugadores involucrados y en que minutos, para pdoer utilizarlos en el dashboard.

El resulttado de la transformación se almacena en un csv (de momento no se guarda en una base de datos), con todo el formato requerido.

Se diseña una aplicación de streamlit, bastante sencilla que toma los datos que se transformaton para alimentar al modelo llm (se esta utilizando gemini) y para generar los graficos.

## ¿Como ejecutar el proyecto?

[Instalar](https://docs.python.org/es/3.13/using/windows.html) Python, dependiendo de el sistema operativo los pasos a seguir son diferentes. 

Crear un entorno virtual, se puede utilizar vs code para mayor comodidad e instalar los requirements.txt
- sudo apt install pipenv
- pipenv install o 
- pipenv install -r requirements.txt

Obtener el api key de gemini en https://aistudio.google.com/apikey

- Ejecutar python ETL/store_page.py  para obtener el html de la página.
- Ejecutar python ETL/matches.py  para obtener información de los partidos.
- Ejecutar python ETL/read_tables.py  para obtener los eventos de los partidos.
- Ejecutar python ETL/transform_data.py  para procesar y unir los datos.
- Ejecutar streamlit run dashboard/app.py  para ver el dashboard.