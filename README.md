
## ¿Cómo se construyó la mini demo?
Se realizó una extracción de datos directamente de la página https://southern-football-league.co.uk/team/Harborough/2385/2024/2025/Py se almacenó la información en un archivo HTML para evitar hacer peticiones recurrentes a la fuente.

Se le dio una estructura a la información, generando un CSV que separa la información de los partidos, los eventos, los minutos, los jugadores involucrados y en qué minutos, para poder utilizarlos en el dashboard.

El resultado de la transformación se almacenó en un CSV (de momento no se guarda en una base de datos), con todo el formato requerido.

Se diseñó una aplicación de Streamlit, bastante sencilla que toma los datos que se transformaron para alimentar al modelo LLM (se está utilizando Gemini) y para generar los gráficos.

## ¿Cómo ejecutar el proyecto?
Instalar Python, dependiendo del sistema operativo los pasos a seguir son diferentes.

Crear un entorno virtual, se puede utilizar VS Code para mayor comodidad e instalar los requirements.txt:

- sudo apt install pipenv

- pipenv install 

o

- pipenv install -r requirements.txt

- Obtener el API key de Gemini en https://aistudio.google.com/apikey

- Ejecutar python ETL/store_page.py para obtener el HTML de la página.

- Ejecutar python ETL/matches.py para obtener información de los partidos.

- Ejecutar python ETL/read_tables.py para obtener los eventos de los partidos.

- Ejecutar python ETL/transform_data.py para procesar y unir los datos.

- Ejecutar streamlit run dashboard/app.py para ver el dashboard.