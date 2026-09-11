import os 
import requests
from dotenv import load_dotenv
from urllib.parse import quote
from database import SessionLocal, Match, PlayerPerformance

#Cargamos el entorno en primer lugar
load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY") #Cogemos la clave del fichero .env

#Utilizamos una cabecera para hacer las peticiones
headers = {'X-Riot-Token': RIOT_API_KEY}

def get_puuid(game_name: str, tag, region: str = 'europe'):
	"Obtener el PUUID a partir del nombre de invocador y la etiqueta"
	url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag}"
	response = requests.get(url, headers= headers)

	if response.status_code != 200:
		print(f"Error al obtener el PUUID: {response.status_code} - {response.text}")
		return

	data = response.json()
	return data['puuid']

def fetch_and_store_matches(puuid: str, region: str = 'europe'):
	# 1.Obtener los IDs de las útlimas partidas del jugador (por defecto solo podemos hacer 5)
	url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=50"
	response = requests.get(url, headers = headers)

	if response.status_code != 200:
		print("No se ha podido extraer la información correctamente")
		return

	matchs_ids = response.json()
	session = SessionLocal()

	for match_id in matchs_ids:
		exists = session.query(Match).filter_by(match_id=match_id).first() #Comprobamos que no exista ya para no duplicarnos 

		if exists:
			print(f"La partida {match_id} ya existe en la base de datos.")
			continue

		match_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
		match_result = requests.get(match_url, headers= headers)

		if match_result.status_code != 200:
			print("No se ha podido obtener la información de la partida correctamente")

		match_data = match_result.json()
		info = match_data["info"]

		game_duration = info["gameDuration"]
		patch = info["gameVersion"]

		# Determinar el equipo ganador (100 o 200)
		winner_team = 100
		for team in info["teams"]:
			if team["win"] and team["teamId"] == 200:
				winner_team ==200

		#Guardamos la partida principal respetando la estructura que hemos definido previamente en nuestra base de datos
		new_match = Match(
			match_id = match_id,
			game_duration = game_duration,
			winner = winner_team,
			patch = patch
		)
		session.add(new_match)

		#Guardamos el rendimiento del jugador
		for participant in info["participants"]:
			new_player = PlayerPerformance(
				match_id = match_id,
				champion_id = participant["championId"],
				team = participant["teamId"],
				kills = participant["kills"],
				deaths = participant["deaths"],
				assists = participant["assists"],
				gold_earned = participant["goldEarned"],
				win = participant["win"]
			)
			session.add(new_player)

		print(f"Partida {match_id} guardada con éxito en la base de datos.")

	session.commit()
	session.close() #Subimos los cambios y cerramos sesión

if __name__ == "__main__":
	GAME_NAME = input("Introduce el game name: ")
	TAG = input("Introduce el tag: ")

	puuid = get_puuid(GAME_NAME, TAG)

	if puuid:
		fetch_and_store_matches(puuid)