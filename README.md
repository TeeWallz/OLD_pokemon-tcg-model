Project Main Goals:
* Ability to easily view data integrity issues in the Pokemon TCG API github json
* To be able to perform data changes 'on top of' the current data via an overlapping stage
    * And to then view and test the resulting data 
    * Best case - via a GUI/web front endS
* To read in new data from other data sources to create an automated 'stage' on top of the base data
* The ability to save this 'diff' to disk/SQL without changing source data

* Reacts ite that runs purely off the github JSON
* and you can edit it just on the site


Current Goals:

* Read in JSON from github into SQLite database
* Create DBT tests to make sure data is OK
* Create python module to allow for staged changes to data
* Ability to export these changes to another JSON file structure


Current questions:
* How to organise python structure for reading in JSON nested objects
* Should the data be read into SQL and only accessed via SQL Alchemy
* Should it stored into SQL, read into data objects, manipulated and saved back?
* Should this be done via a main Class with methods to do the dirty work?
* Should DBT just be used for tests? If reading is done via Python, what use does DBT have?
* How could this be more accessible for other users?
* How can this be used to 'stage' new changes over existing data and preview it


* Could this be done via reading the JSON into a mongoDB in a React project? 