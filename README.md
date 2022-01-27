# Intelligentes Paketmanagement
Das Ziel dieses Projektes ist es, ein System zu entwickeln, welches eine sortierte
Reihenfolge von Paketen ermittelt, woraus schließlich eine optimale Route entsteht.
Die Route soll unter anderem eine Priorisierung von beispielsweise sehr schweren
oder sehr großen Paketen zulassen.
In diesem Projekt wwerden Pakete auf Basis von Adressdaten und synthetisch
generierten Paketdaten mithilfe von Machine Learning priorisiert und sortiert, 
sodass sich eine optimale Route ergibt. Der oder die Paketzusteller*in
spart damit einiges an Zeit bei der Beladung und der Auslieferung der Pakete.
Dies zeigt, dass sich die Effizienz von Paketzusteller*innen durch die automati-
sierte Sortierung und Priorisierung der Pakete erheblich steigern lässt. Auf dieser
Grundlage ist es empfehlenswert, Machine Learning im Bereich der Paketzustellung
einzusetzen, um Arbeitszeiten und dadurch entstehende Kosten zu sparen.

## Create Python Environment
This chapter describes the necesseray steps, so all of the developers have the same python environment:

### Requirements:
* Python 3.8.8 -> https://www.python.org/downloads/release/python-388/
* Pip
* PyCharm
* Docker -> [install here on Windows](https://docs.docker.com/desktop/windows/install/)
* MongoDB-Atlas-Account -> [register for free](https://www.mongodb.com/de-de/cloud/atlas/register)
* NodeJs -> [Download here](https://nodejs.org/en/download/)

### Installation and Startup
1. clone the git repository
2. open PyCharm
	* File -> open 
		* select the git repository
	* view Terminal in PyCharm -> check if the  virtualenv is acticated (should be but you never know)
		* the line should look like: (Project name) Path 
	* if the virtualenv is not activated proceed with the following steps:
		* in the pycharm terminal navigate into the roject package and enter the following command:
			* name of the environment\Scripts\activate (if this doesn't work try <name of the environment>\Scripts\activate.bat)
		* your terminal line now should look like: (Project name) Path
	* check if the correct python interpreter is used 
		* on the bottom rigth corner you can see the branch and left from it you can see the python interpreter that is used. If it is the wrong one, click on it and change it to the correct one
			* if it doesn't appear in the list click on interpreter settings
			* then click on the settings symbol and then on add -> add the correct python interpreter and select it

3. start Docker	
* Under the Directory Neo4j execute following command `docker-compose up -d`  
* Neo4j should be running now. You can test the connection under http://localhost:7687	
* Replace the Connection String in init.py under Neo4j with your own Connection-String

4. Sign in with your [MongoDB-Account](https://account.mongodb.com/account/login)
* Create shared Cluster with Database and Collection -> [View Documentation](https://docs.atlas.mongodb.com/getting-started/)
* Copy Connection String
* Under the Directory Route_Computation replace MongoDB-Connnection String with your own Connection-String 	
and replace the default params with your own Credentials.
* The same procedure applies to the server.ts file unter frontend/Server.

5. Run `python api.py` in the root-Directory
6. Api should now be accessible at http://localhost:5000
7. Route Computation can now be triggered at http://localhost:5000/compute-route?post_station_id=value&district=value&date=value
### Pip usage
* you can view the list of installed packages via pip list
* it is important that all developers work with the same pip packages. The easiest way to do this is with a requirements file.
	* to export a requirements file type into the terminal: 
		* pip freeze > requirements.txt
	* to import a requirements file use:
		* pip install -r requirements.txt
	* __the requirements file in git should always be the latest__

### Neo4j
* http://192.52.37.239:7474/
