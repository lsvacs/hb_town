import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

df_ = pd.read_csv('data/cleaned_hb.csv')
df=df_[df_['team']=='Harborough Town']
st.set_page_config(layout="wide")

col1, col2 = st.columns(2)

with col1:
    st.image("dashboard/logo.png")
    st.title('Dashboard con Streamlit y Plotly')
    st.write('Distribución de los datos')

with col2:
    tipo_registro = st.selectbox('Selecciona el tipo de registro', ["Goal", "Caution", "Substitution", "Red Card"])

    df_filtrado = df[df['event_action'] == tipo_registro]

    fig_ = px.histogram(df_filtrado, x='mins', nbins=20, title=f'Histograma de {tipo_registro}')

    st.plotly_chart(fig_)

with col1:
    key = st.text_input('gemini key')
    prompt = st.text_input('Input question about Harborough (try to be specific. Ex. Cual es el jugador con mas Caution)')
    if prompt and key:
        with col1:
            print("Starting agent")
            agent = create_pandas_dataframe_agent(
                ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=3,
                    google_api_key=key
                    # google_api_key=""
                ),
                df,
                verbose=True,
                allow_dangerous_code=True
            )
            try:
                output=agent.invoke(prompt)
            except Exception as e:
                print("Error: {e}")
                output['output']="Quota error re try."
            st.write(output['output'])

with col1:
    probabilidades = pd.DataFrame(columns=['event_action', 'Victoria', 'Empate', 'Derrota'])


    eventos_interes = ['Red Card', 'Goal', 'Caution']
    df_eventos = df[df['event_action'].isin(eventos_interes)]
    df_resultados = df[['identifier', 'Resultado']].drop_duplicates()
    df_frecuencia = df_eventos.groupby(['identifier', 'event_action']).size().unstack(fill_value=0)
    df_frecuencia = df_frecuencia.merge(df_resultados, on='identifier')


    contingency_table = pd.crosstab(index=[df_frecuencia['Caution'], df_frecuencia['Red Card'], df_frecuencia['Goal']], columns=df_frecuencia['Resultado'])

    st.write("### Análisis de Contingencia")
    st.write(contingency_table)

    caution_values = contingency_table.index.get_level_values('Caution').unique()
    red_card_values = contingency_table.index.get_level_values('Red Card').unique()
    goal_values = contingency_table.index.get_level_values('Goal').unique()

    selected_caution = st.selectbox('Selecciona el valor de Caution', options=[None] + list(caution_values))
    selected_red_card = st.selectbox('Selecciona el valor de Red Card', options=[None] + list(red_card_values))
    selected_goal = st.selectbox('Selecciona el valor de Goal', options=[None] + list(goal_values))

    contingency_table_filter = contingency_table

    if selected_caution is not None:
        contingency_table_filter = contingency_table_filter.xs(selected_caution, level='Caution')
    if selected_red_card is not None:
        contingency_table_filter = contingency_table_filter.xs(selected_red_card, level='Red Card')
    if selected_goal is not None:
        contingency_table_filter = contingency_table_filter.xs(selected_goal, level='Goal')

    st.write("### Resultados Filtrados")
    if not contingency_table_filter.empty:
        st.write(contingency_table_filter)
    else:
        st.write("No hay resultados para esa combinacion")


with col2:
    mean_values = {
        'Caution': df_frecuencia['Caution'].mean(),
        'Goal': df_frecuencia['Goal'].mean(),
        'Red Card': df_frecuencia['Red Card'].mean()
    }

    fig_caution = px.histogram(
        df_frecuencia, 
        x="Caution", 
        color="Resultado", 
        title="Distribución de Caution",
        labels={"Caution": "Caution", "count": "Frecuencia"},
        hover_data=["Resultado"],
        color_discrete_map={
        "derrota": "#CF1800",  # Azul
        "victoria": "#2F4858",  # Verde
        "empate": "#33658A"   # Amarillo
    }
    )
    fig_caution.add_vline(x=mean_values["Caution"], line=dict(color="red", dash="dash"), 
                        annotation_text=f"Media Caution: {mean_values['Caution']:.2f}", 
                        annotation_position="top right")
    fig_caution.update_layout(showlegend=True)

    fig_goal = px.histogram(
        df_frecuencia, 
        x="Goal", 
        color="Resultado", 
        title="Distribución de Goal",
        labels={"Goal": "Goal", "count": "Frecuencia"},
        hover_data=["Resultado"],
        color_discrete_map={
        "derrota": "#CF1800",  # Azul
        "victoria": "#2F4858",  # Verde
        "empate": "#33658A"   # Amarillo
    }
    )
    fig_goal.add_vline(x=mean_values["Goal"], line=dict(color="red", dash="dash"), 
                    annotation_text=f"Media Goal: {mean_values['Goal']:.2f}", 
                    annotation_position="top right")
    fig_goal.update_layout(showlegend=True)

    fig_red_card = px.histogram(
        df_frecuencia, 
        x="Red Card", 
        color="Resultado", 
        title="Distribución de Red Card",
        labels={"Red Card": "Red Card", "count": "Frecuencia"},
        hover_data=["Resultado"],
        color_discrete_map={
        "derrota": "#CF1800",  # Azul
        "victoria": "#2F4858",  # Verde
        "empate": "#33658A"   # Amarillo
    }
    )
    fig_red_card.add_vline(x=mean_values["Red Card"], line=dict(color="red", dash="dash"), 
                        annotation_text=f"Media Red Card: {mean_values['Red Card']:.2f}", 
                        annotation_position="top right")
    fig_red_card.update_layout(showlegend=True)

    st.plotly_chart(fig_caution)
    st.plotly_chart(fig_goal)
    st.plotly_chart(fig_red_card)
