# Intelligentes Paketmanagement

## Create Python Environment
This chapter describes the necesseray steps, so all of the developers have the same python environment:

### Requirements:
* Python 3.8.8 -> https://www.python.org/downloads/release/python-388/
* Pip
* PyCharm

### Installation
* clone the git repository
* open PyCharm
	* File -> open 
		* select the git repository
	* view Terminal in PyCharm -> check if the  virtualenv is acticated 
		* the line should look like: (Project name) Path 
	* if the virtualenv is not activated proceed with the following steps:
		* in the pycharm terminal navigate into the roject package and enter the following command:
			* <name of the environment>\Scripts\activate (if this doesn't work try <name of the environment>\Scripts\activate.bat)
		* your terminal line now should look like: (Project name) Path

### Pip usage
* you can view the list of installed packages via pip list
* it is important that all developers work with the same pip packages. The easiest way to do this is with a requirements file.
	* to export a requirements file type into the terminal: 
		* pip freeze > requirements.txt
	* to import a requirements file use:
		* pip install -r requirements.txt
	* __the requirements file in git should always be the latest__
