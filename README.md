# LoL_Match_Predictor

El proyecto consiste en el diseño y desarrollo de una plataforma completa de ingeniería de datos y Machine Learning aplicada al análisis predictivo de partidas clasificadas de League of Legends. El objetivo principal es construir un sistema capaz de recopilar datos históricos de partidas de alto nivel competitivo (Challenger, Grandmaster y Master), almacenarlos mediante una arquitectura de datos profesional, transformarlos en variables analíticas y finalmente entrenar un modelo de aprendizaje automático que permita estimar la probabilidad de victoria de un equipo antes del inicio de la partida (durante la fase de selección de campeones).

La motivación principal del proyecto surge de la gran cantidad de información disponible en videojuegos competitivos modernos. En títulos como League of Legends, cada partida genera cientos de variables relacionadas con campeones seleccionados, runas, hechizos de invocador, historial de los jugadores, oro, objetivos y resultado final. Sin embargo, estos datos en bruto no tienen utilidad directa para la predicción, por lo que es necesario construir un pipeline completo que transforme información no estructurada procedente de la API oficial en datos preparados para análisis y modelado predictivo.

La fuente principal de datos utilizada será la API oficial de Riot Games. El sistema realizará procesos automáticos de extracción mediante peticiones HTTP utilizando Python, gestionando las claves de desarrollo y respetando los límites de velocidad (*rate limiting*) establecidos por los servidores de Riot (por ejemplo, mediante la librería `requests` combinada con control de tiempos o wrappers específicos) para evitar bloqueos y garantizar una ingesta estable.

La primera gran fase del proyecto corresponde a la ingeniería de datos. En esta etapa se construirá un proceso ETL (Extract, Transform, Load) encargado de obtener listas de invocadores en rangos altos mediante los endpoints de ligas (`/lol/league/v4/...`), recuperar sus identificadores únicos (`puuid`), descargar el historial de partidas (`/lol/match/v5/matches/...`) y procesar los documentos JSON anidados para convertirlos en estructuras tabulares mediante Pandas. El pipeline incorporará reglas de validación y limpieza de datos, eliminando partidas de duración anormal (como *remakes*), registros corruptos o entradas que no cumplan los requisitos mínimos necesarios para el análisis.

La información procesada será almacenada en una base de datos relacional PostgreSQL alojada en Neon, utilizando un diseño estructurado basado en separación de responsabilidades. La arquitectura seguirá principios utilizados habitualmente en sistemas analíticos profesionales, separando dimensiones estáticas de tablas de hechos relacionadas con encuentros y rendimiento de jugadores.

La base de datos estará formada principalmente por cuatro componentes:

* **dim_champions**: tabla dimensional que contiene información estática de cada campeón de League of Legends (obtenida mediante Data Dragon), como rol principal, tipo de daño y estadísticas base.
* **matches**: tabla de hechos que almacena información general de cada partida, incluyendo equipo ganador, duración, parche del juego y fecha de inicio.
* **players**: tabla de hechos que contiene el rendimiento individual de cada invocador dentro de una partida, incluyendo campeón seleccionado, posición (top, jungle, mid, bot, support), asesinatos, muertes, asistencias, oro total y daño infligido.
* **champion_statistics**: tabla agregada generada a partir de los datos históricos, utilizada para obtener métricas como porcentaje de victoria, tasa de selección (*pick rate*), tasa de prohibición (*ban rate*) y rendimiento medio de cada campeón.

Una vez consolidada la información histórica, comenzará la fase de ciencia de datos. El objetivo será transformar los datos almacenados en un conjunto de características (*features*) adecuadas para un modelo de clasificación supervisada. El modelo tendrá como variable objetivo la victoria o derrota de un equipo y utilizará información disponible antes del comienzo de la partida (como los campeones elegidos por ambos lados y las estadísticas agregadas de los jugadores), evitando problemas de fuga de información (*data leakage*).

El desarrollo del modelo predictivo se realizará utilizando herramientas de Machine Learning en Python, principalmente Scikit-learn. Se comenzará con modelos base interpretables, como Regresión Logística, para establecer una referencia inicial, y posteriormente se evaluarán algoritmos más avanzados como Random Forest o Gradient Boosting (XGBoost / LightGBM).

Finalmente, el modelo será integrado dentro de una aplicación web interactiva desarrollada con Streamlit. Esta interfaz permitirá al usuario seleccionar la composición de campeones de ambos equipos (Draft Simulator) y obtener una estimación en tiempo real de la probabilidad de victoria basada en el modelo entrenado. La aplicación funcionará como una capa de presentación sobre todo el sistema construido previamente.

El resultado final será una arquitectura completa de datos que representa un flujo profesional de extremo a extremo:

Riot Games API
|
|
v
Python ETL Pipeline
|
|
v
PostgreSQL Neon Database
|
|
v
Data Analysis & Feature Engineering
|
|
v
Machine Learning Model
|
|
v
Streamlit Prediction Dashboard

### Tecnologías utilizadas y previstas

#### Lenguaje principal

* **Python**: Lenguaje central del proyecto para el consumo de APIs, transformación de datos, conexión con bases de datos, creación del pipeline ETL, entrenamiento del modelo y desarrollo de la interfaz web.

#### Fuente de datos

* **Riot Games API**: Plataforma oficial de desarrollo que proporciona acceso a las colas clasificadas, estadísticas de invocadores e historiales de partidas a través de los servicios de Match-V5 y League-V4.
* **Data Dragon**: Servicio estático de Riot para la descarga de recursos y metadatos actualizados de campeones, objetos y hechizos en formato JSON.

#### Procesamiento de datos

* **Pandas**: Utilizado para la manipulación de DataFrames, limpieza de datos, normalización de JSON anidados y preparación de datasets.
* **Requests**: Utilizado para realizar peticiones HTTP seguras y gestionar la comunicación con los servidores de la API de Riot.

#### Base de datos

* **PostgreSQL**: Motor relacional robusto para garantizar la integridad referencial y permitir consultas analíticas complejas.
* **Neon**: Servicio gestionado de PostgreSQL en la nube, idóneo para entornos de desarrollo escalables y despliegues en portfolio.
* **SQLAlchemy**: Capa de abstracción de bases de datos (*ORM*) en Python para gestionar la conexión, sesiones y operaciones sobre PostgreSQL.

#### Machine Learning

* **Scikit-learn**: Utilizado para la preprocesamiento de variables, codificación de campeones, entrenamiento de clasificadores y evaluación de métricas de rendimiento.

#### Visualización y despliegue

* **Streamlit**: Framework para construir y desplegar la aplicación web interactiva del simulador de *drafts* y visualización de probabilidades.

#### Control de versiones

* **Git + GitHub**: Utilizados para el control de cambios, documentación del repositorio y estructuración del proyecto con estándares de código profesional.
