import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from database import engine

def train_prediction_model():
    # 1. Cargar el rendimiento de los jugadores junto con las partidas
    query = """
        SELECT 
            p.match_id,
            p.team,
            p.champion_id,
            p.kills,
            p.deaths,
            p.assists,
            p.gold_earned,
            p.win
        FROM players p;
    """
    df = pd.read_sql(query, con=engine)
    
    if df.empty:
        print("No hay suficientes datos en la base de datos para entrenar el modelo.")
        return

    # 2. Transformar los datos: Agrupar por partida y equipo para sumar métricas de bando
    # Equipo 100 vs Equipo 200
    match_grouped = df.groupby(['match_id', 'team']).agg(
        total_kills=('kills', 'sum'),
        total_deaths=('deaths', 'sum'),
        total_assists=('assists', 'sum'),
        total_gold=('gold_earned', 'sum'),
        won=('win', 'first') # Si un jugador ganó, el equipo ganó
    ).reset_index()

    # Separar en Equipo 100 y Equipo 200 para estructurar la partida en una sola fila
    team_100 = match_grouped[match_grouped['team'] == 100].drop(columns=['team'])
    team_200 = match_grouped[match_grouped['team'] == 200].drop(columns=['team'])

    # Renombrar columnas para fusionarlas
    team_100 = team_100.rename(columns={c: f"t100_{c}" for c in team_100.columns if c != 'match_id'})
    team_200 = team_200.rename(columns={c: f"t200_{c}" for c in team_200.columns if c != 'match_id'})

    # Unir ambos equipos por match_id
    ml_df = pd.merge(team_100, team_200, on='match_id')
    
    if ml_df.empty:
        print("No hay suficientes partidas completas de ambos equipos para cruzar.")
        return

    # Definir Variables Predictoras (X) y la Variable Objetivo (y) -> ¿Gana el equipo 100? (1 o 0)
    # Nota: Usamos métricas de oro/kills pasadas o simuladas. Para un modelo real pre-partida, 
    # usaríamos solo los campeones elegidos, pero este es tu modelo base de prueba.
    X = ml_df[['t100_total_gold', 't200_total_gold', 't100_total_kills', 't200_total_kills', '']]
    y = ml_df['t100_won'].astype(int)

    if len(ml_df) < 5:
        print(f"\nTienes {len(ml_df)} partidas procesadas. Se recomienda tener al menos 20-50 partidas para que el modelo aprenda con sentido.")
        print("¡Sube el count en load_matches.py para descargar más historial y vuelve a ejecutar esto!")
        return

    # 3. Dividir datos en entrenamiento y testeo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Entrenar el modelo de Machine Learning (Random Forest)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluar precisión
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)

    print(f"--- RESULTADO DEL MODELO ---")
    print(f"Partidas totales analizadas para ML: {len(ml_df)}")
    print(f"Precisión del modelo (Accuracy): {acc * 100:.2f}%")

if __name__ == "__main__":
    train_prediction_model()