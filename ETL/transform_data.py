import pandas as pd
import re


df = pd.read_csv("data/harborough.csv")

def extract_first_value(text):
    match = re.search(r'([A-Za-z\s]+)(?=[:!])', text)
    return match.group(0) if match else None

def extract_final_value(text):
    if text.startswith('Goal!'):
        patron = r"for (.+?)!"
        resultado = re.search(patron, text)
        if resultado:
            nombre = resultado.group(1)
            return nombre
    else: 
        match = re.search(r'\(([^)]+)\)$', text)
        return match.group(1) if match else None

df['event_action'] = df['event'].apply(extract_first_value)
df['team_event'] = df['event'].apply(extract_final_value)


def extract_names(text):
    if text.startswith(('Caution:', 'Red Card:')):
        match = re.search(r': ([^:]+?) of', text)
        name1 = match.group(1) if match else None
        return name1, None
    elif text.startswith('Substitution:'):
        match1 = re.search(r': (\d+): ([^:]+?) of', text)
        match2 = re.search(r'replaced by \d+: ([^:]+?) \(', text)
        name1 = match1.group(2) if match1 else None
        name2 = match2.group(1) if match2 else None
        return name1, name2
    elif text.startswith(('Goal!', 'Oh no!')):
        match = re.search(r'! ([^!]+?) scores|! ([^!]+?) OG', text)
        name1 = match.group(1) if match else match.group(2)
        return name1, None
    else:
        return None, None

df[['name1', 'name2']] = df['event'].apply(lambda x: pd.Series(extract_names(x)))

def extract_attendance(text):
    match = re.search(r'(\d+)$', text)
    attendance = match.group(1) if match else None
    return attendance

df["attendance"] = df['event'].apply(extract_attendance)

def evaluar_y_convertir(valor):
    try:
        return int(eval(valor))
    except:
        return valor

df['mins'] = df['mins'].apply(evaluar_y_convertir)

matches_df = pd.read_csv("data/matches.csv")

df = df.merge(matches_df, on='identifier', how='left')

df = df.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])

def determinar_resultado(row):
    if row['event_action']:
        if 'Final whistle' in row['event_action']:
            score_local, score_visitante = map(int, row['score'].split('-'))
            if score_local > score_visitante:
                return "victoria" if row['team']=="Harborough Town" else "derrota"  
            elif score_local < score_visitante:
                return "victoria" if row['match'].replace(f"row['team'] v ", '').strip()=="Harborough Town" else "derrota"  
            else:
                return 'empate'
    return None

df['Resultado'] = df.apply(determinar_resultado, axis=1)

df['Resultado'] = df.groupby('identifier')['Resultado'].ffill().bfill()

df.to_csv("data/cleaned_hb.csv")