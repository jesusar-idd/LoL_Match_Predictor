import requests
from database import SessionLocal, DimChampion

def fetch_and_store_champions():
	# 1.Obtendremos la última versión del juego
	version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
	versiones = requests.get(version_url).json()
	latest_version = versiones[0] #Cogemos la última versión

	champion_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
	response = requests.get(champion_url)

	if response.status_code != 200: #Manejamos el error en caso que no sea posible descargar los datos de los campeones
		print("Error al descargar el catálogo de los campeones")
		return

	data = response.json()["data"]
	session = SessionLocal()

	count = 0 #Iniciamos un conteo a 0
	for champ_name, champ_info in data.items():
		champ_id = int(champ_info['key'])
		name = str(champ_info['name'])
		roles = ", ".join(champ_info['tags'])

		#Manejamos que no existan duplicados
		exists = session.query(DimChampion).filter_by(id=champ_id).first()
		if not exists:
			new_champ = DimChampion(id=champ_id, name=name, role=roles)
			session.add(new_champ)
			count +=1

	session.commit()
	session.close()
	#Finalmente enviamos un mensaje para comprobar que hemos realizado todo el proceso correctamente 
	print(f"¡Se han guardado {count} campeones correctamente en la tabla dim_champions!")

if __name__ == "__main__":
    fetch_and_store_champions()