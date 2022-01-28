# Intelligentes Paketmanagement
Das Ziel dieses Projektes ist es, ein System zu entwickeln, welches eine sortierte Reihenfolge von Paketen ermittelt, woraus schließlich eine optimale Route entsteht. Die Route soll unter anderem eine Priorisierung von beispielsweise sehr schweren oder sehr großen Paketen zulassen.

In diesem Projekt werden Pakete auf Basis von Adressdaten und synthetisch generierten Paketdaten mithilfe von Machine Learning priorisiert und sortiert, sodass sich eine optimale Route ergibt. Der oder die Paketzusteller:in spart damit einiges an Zeit bei der Beladung und der Auslieferung der Pakete.

Dies zeigt, dass sich die Effizienz von Paketzusteller:innen durch die automati sierte Sortierung und Priorisierung der Pakete erheblich steigern lässt. Auf dieser Grundlage ist es empfehlenswert, Machine Learning im Bereich der Paketzustellung einzusetzen, um Arbeitszeiten und dadurch entstehende Kosten zu sparen.

## Create Python Environment
This chapter describes the necesseray steps, so all of the developers have the same python environment:

### Requirements:
This project was build with the following tools in the specified versions:
* Python 3.8.8 -> https://www.python.org/downloads/release/python-388/
* Pip
* PyCharm
* Docker -> [install here on Windows](https://docs.docker.com/desktop/windows/install/)
* MongoDB-Atlas-Account -> [register for free](https://www.mongodb.com/de-de/cloud/atlas/register) or local installation of MongoDB
* NodeJs -> [Download here](https://nodejs.org/en/download/)

### Installation and Startup
1. clone this git repository
2. Open your IDE (we used PyCharm) and create a virtualenv. Then use the `requirements.txt` to get all the python packages we used. (in your console in the root-directory execute the following pip-command: `pip install -r requirements.txt`)
3. Start Docker	
* Under the Directory Neo4j execute the following command: `docker-compose up -d`  
* Neo4j should be running now. You can test the connection under `http://localhost:7687`
* In the root-Directory create a `Passwords.py` file. This file is mentioned in the .gitignore an will not be synced to the repo...
* Replace the Connection String, username and password in `Passwords.py` with your own credentials. You need to create 3 methods (they should be named exactly like the following declaration, otherwise you need to change the Python Scripts):
    * `def get_uri()` which returns your uri as a String
    * `def get_user()` which returns your username as a String
    * `def get_password()` which returns your password as a String
4. MongoDB
* MongoDB-Atlas:
    * Sign in with your [MongoDB-Account](https://account.mongodb.com/account/login)
    * Create shared Cluster with Database and Collection -> [View Documentation](https://docs.atlas.mongodb.com/getting-started/)
    * Copy Connection String
    * In the `Passwords.py` add antoher method `def get_mongodb_connection_string()` which returns your Connection-String 
    * Replace the Connection-String under `frontend/Server` in the `server.ts` with your own Connection-String
* local MongoDB installation:
    * Start MongoDB-Server
    * Copy Connection String
    * In the `Passwords.py` add antoher method `def get_mongodb_connection_string()` which returns your Connection-String 
    * Replace the Connection-String under `frontend/Server` in the `server.ts` with your own Connection-String
5. API 
* Open terminal and run `python api.py` in the root-Directory
* Api should now be accessible at `http://localhost:5000`
* Route Computation can now be triggered at `http://localhost:5000/compute-route?post_station_id=value&district=value&date=value`
* Package (`http://localhost:5000/add-package`) and Addressdata (`http://localhost:5000/add-address`) can also be send to the API as JSON-Objects
6. Frontend
* In the terminal go to the directory `frontend/Server` and execute the command `npm start`
* Now navigate to the directory `frontend/Client` and open the `index.html`
* Your standard-browser should open with the frontend