import pandas as pd
from database import engine

def matches_data_analysis():
	# Debemos consultar en primer lugar en SQL para unir las tablas de rendimiento, campeones y partidas
	query = """
			SELECT 
				p.match_id,
				c.name AS champion_name,
				c.role AS champion_roles,
				p.team,
				p.kills,
				p.deaths,
				p.assists,
				p.gold_earned,
				p.win
			FROM players p
			JOIN dim_champions c ON p.champion_id = c.id;
			"""

	df = pd.read_sql(query, con=engine)

	if df.empty:
		print("No se encuentran jugadores en la base de datos")
		return

	print("RESUMEN DE LOS DATOS DE LA ÚLTIMA PARTIDA")
	print(df.head(10))

	print("TASA DE VICTORIA POR CAMPEÓN")
	champ_stats = df.groupby('champion_name').agg(
		total_games = ('win', 'count'),
		wins = ('win', lambda x: x.sum()),
		avg_kills=('kills', 'mean'),
		avg_deaths=('deaths','mean')
	)

	champ_stats['win_rate'] = (champ_stats["wins"] / champ_stats["total_games"]) *100
	champ_stats = champ_stats.sort_values(by="total_games", ascending=False)

	print(champ_stats.round(2))

if __name__=="__main__":
	matches_data_analysis()	