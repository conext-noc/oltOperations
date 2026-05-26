# DEVELOPING:

### VENV #

- Use of virtualenvs:
  Virtual environments in Python are a best practice that allows you to create isolated environments to work on specific Python projects. Here are some reasons why you should use virtual environments in Python:

  1. Isolation: Virtual environments allow you to create a completely isolated environment for each project you are working on. This means that any packages you install or dependencies you add will only be installed in that specific environment and not affect your global Python installation.
  2. Reproducibility: By creating a virtual environment for each project, you can ensure that your project's dependencies are consistent and reproducible. This makes it easier for others to replicate your project and for you to work on it in the future.
  3. Dependency management: Managing dependencies can be a challenging task, especially when working on multiple projects simultaneously. Virtual environments help to simplify this process by allowing you to easily install and manage dependencies for each project.
  4. Version control: Virtual environments make it easier to use version control tools like Git. By including your virtual environment in your project's repository, you can ensure that anyone who clones your repository can easily set up the same environment as you.

  Overall, virtual environments in Python help to create a more organized, reproducible, and efficient workflow.

> In case that virtualenv is not installed by pip
```terminal
[bash]$ pip install virtualenv
```
> adding a virtual env
```terminal
[bash]$ python -m virtualenv <virtual enviroment folder name>
```

### CLONING AND SETUP

For clonning this project issue the command:
```terminal
[bash]$ git clone https://github.com/conext-noc/oltOperations.git
```
OR if you have the ssh key and set up ssh with github with your account.
```terminal
[bash]$ git clone git@github.com:conext-noc/oltOperations.git
```

then download the [.env, service_account_olt_operations.json] files from the conext noc drive folder located in the IT>SCRIPTS folder or simply ask for them if you work at the tech department.

once those files are downloaded and put in this directory set up the virtual env.

once the virtual env is placed use the following command:
```terminal
[bash]$ source ./`<venv folder name>`/bin/activate
```
then install all deps:
```terminal
[bash]$ pip install -r requirements.txt
```
then all is set for usage or development.

### FOLDER STRUCTURE:

this is the current folder structure & file meaning:
```folder
📦helpers   //   this folder contains helper modules to simplify tasks across the script an the main modules
 ┣ 📂clientFinder   //   this folder contains clients data related
 ┃ ┣ 📜dataLookup.py   //   this file retrives the info of a client (run_state, control_flag, etc...)
 ┃ ┣ 📜lookup.py   //   this file is the one in charge of getting and formatting all the clients data
 ┃ ┣ 📜nameLookup.py   //   this file searches in olt all the clients that matches the given name
 ┃ ┣ 📜newLookup.py   //   this file searches in the olt all the available ONT to confirm and returns the slot and port if the SN matches
 ┃ ┣ 📜ontType.py   //   this module finds the type of ont
 ┃ ┣ 📜optical.py   //   this module request the current optical values of the ONT
 ┃ ┣ 📜serialLookup.py   //   this module searches the given SN in the OLT and retrives the data
 ┃ ┣ 📜wan.py   //   this module collects all the wan info of a client
 ┃ ┗ 📜wanInterface.py   //   this module finds which vlan has been issued in the ONT
 ┣ 📂failHandler   //   this folder contain fail handler module
 ┃ ┗ 📜fail.py   //   this file's only task is to lookout for potential failures that may occur when dealing with ssh lines in th olt
 ┣ 📂fileFormatters   //   this folder contains file handler modules
 ┃ ┣ 📜fileHandler.py   //   this module rectifies the data and sendsit back in the requested format (dict, lists, files (xlsx, csv))
 ┃ ┗ 📜table.py   //   this module formats the ssh lines into a dictionary when needed (for port related queries)
 ┣ 📂info   //   this folder conatains information / regex info modules
 ┃ ┣ 📜hashMaps.py   //   this file holds all the hash maps of the project
 ┃ ┣ 📜plans.py   //   this file holds a dictionary of all the plans used
 ┃ ┗ 📜regexConditions.py   //   this file holds all the regex conditions for quering the data
 ┣ 📂operations   //   this folder contains client operation modules
 ┃ ┣ 📜addHandler.py   //   this module adds a client to the OLT and adds the corresponding service to that client
 ┃ ┗ 📜spid.py   //   this module calculates the corresponding Service Port ID for that clients location and service type in the olt (F/S/P/ID)
 ┗ 📂utils   //   this folder contains general purpouse modules
 ┃ ┣ 📜decoder.py   //   this module decodes the incomming bytes of the ssh lines
 ┃ ┣ 📜display.py   //   this module only displays the queried data into the terminal
 ┃ ┣ 📜interfaceHandler.py   //   this module returns the info of the router interface into a well formatted data structure
 ┃ ┣ 📜printer.py   //   this module prints out the data, formats into colors and gets user input data and redirects it to the terminal and into the log file
 ┃ ┣ 📜sheets.py   //   this module handles the comunication and file management of CPDC in the google sheet file
 ┃ ┣ 📜ssh.py   //   this file handles the communication for ssh lines
 ┃ ┣ 📜template.py   //   this file has templates for instaling clients and requesting data of the clients
 ┃ ┗ 📜verify.py   //   this file verifies that a client has been reactivated or deactivated properly
📦scripts   //   this fo;der contains the main usage scripts
 ┣ 📜__init__.py   //   this is an initializer empty file
 ┣ 📜AD.py   //   this module upgrades the data of the clients in a mass way in case is needed
 ┣ 📜BC.py   //   this module finds all the data regarding of a single client
 ┣ 📜CPDC.py   //   this module creates the CPDC.xlsx file [data of every client in the selected OLT]
 ┣ 📜EC.py   //   this module deletes completely a client from the OLT
 ┣ 📜IX.py   //   this module adds | confirms a client in the OLT
 ┣ 📜MC.py   //   this module modifies a clients data [vlan, data plan, name, ont, etc...]
 ┣ 📜MG.py   //   this module if for the migration only
 ┣ 📜OLT.py   //   this is the main OLTS access module
 ┣ 📜OX.py   //   this module reactivates and deactivates a list of clients or a single client
 ┣ 📜RTR.py   //   this is the main ROUTERS access module
 ┣ 📜VC.py   //   this module monitors the client data usage @ this given time (ask for the usage 5 times then gives an average)
 ┗ 📜XP.py   //   this module diplays all clients in a given port, all deactivated clients in OLT and all LOS clients in OLT
📦<venv folder>   //   in this folder is stored all dependencies, do not push this folder into the repo
📜.env   //   this file holds the credentials used to SSH into the Conext devices
📜.gitignore   //   this file is the one that ignores certain files, folders and enven file tipes
📜README.dev.md   //   this is this file, it holds information about how to develop, modify and expand modules
📜README.md   //   this file is the user documentation
📜TS.py   //   this file is only for development and should never be in the main script
📜main.py   //   this is the main entry file for the script
📜requirements.txt   //   this file holds the dependency versions
📜service_account_olt_operations.json   //   this file (ignored) holds the creedentials for google cloud to manage files
```


### HOW TO DEVELOP

#### MODULE

for developing a module rename the module in a 2 letter word nomenclature, if the module is used in various places try to rename it into a genreal way to improve DRY code

the fuction of the module should be declare in a declarative methodology, and the same with each part of the code

#### UPDATING/IMPROVING A MODULE

some sort pf the same a developing one just rename the things into a declarative methodology

#### TIPS

> use lower_snake_case for variable names, and for some constants use UPPER_SNAKE_CASE
> for the files use camelCase
> place the variable or regex condition in its corresponding file
