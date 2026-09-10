import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

load_dotenv() #Cargamos en primer lugar los archivos del archivo .env donde tenemos toda la información
DATABASE_URL = os.getenv("DATABASE_URL") #Obtenemos la URL de la base de datos de donde vamos a extraer la información

#Creamos la conexión con Neon (Database de Postgre SQL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DEFINICIÓN DE TABLAS

class DimChampion(Base):
	__tablename__ = "dim_champions"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True) #Nombre del campeón
	role = Column(String) #Rol del personaje

class Match(Base):
    __tablename__ = "matches"
    
    match_id = Column(String, primary_key=True, index=True) # ID único de la partida (ej: EUW1_12345678)
    game_duration = Column(Integer)                         # Duración en segundos
    winner = Column(Integer)                                # 100 para equipo azul, 200 para rojo
    patch = Column(String)                                  # Parche del juego

class PlayerPerformance(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(String, ForeignKey("matches.match_id"))
    champion_id = Column(Integer, ForeignKey("dim_champions.id"))
    team = Column(Integer)                                  # 100 o 200
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    gold_earned = Column(Integer)
    win = Column(Boolean)                                   # True si ganó, False si perdió

# Función para crear las tablas físicamente en Neon
def init_db():
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas correctamente en la base de datos de Neon!")

if __name__ == "__main__":
    init_db()