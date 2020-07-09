Villagers and Heroes API
========================

Code related to the game Villagers &amp; Heroes

Heroku
------
Heroku (www.heroku.com) is used for hosting the application.
- Create the application in Heroku

        $ heroku login
        $ heroku create vnh-api
        $ git push heroku master
        $ heroku ps:scale web=1

- Open the application in a browser (just a shortcut)
        
        $ heroku open

- Viewing logs

        $ heroku logs --tail

- List information about the dynos used

        $ heroku ps
        
- Run locally (CTRL+C to kill)

        $ heroku local

- Upload latest changes to Heroku
    - NOTE: I have updated the configuration on Heroku to automatically deploy when changes are checked in to master, so no need to use the below command anymore

            $ git push heroku master

- Configuration variables
    - Variables can be set on the heroku application that will then be available as environment variables. To list the
    current configuration:
    
            $ heroku config
    
    - To set the configuration variable "TIMES" to "2":
    
            $ heroku config:set TIMES=2

- Bash
    - Connects to the bash prompt on the Heroku server for running commands
        
            $ heroku run bash
        
- Database
    - I set up a PostgreSQL instance to be utilized via the Heroku UI - the connection string can be found in the
    DATABASE_URL configuration variable
    
    - Additionally, I created a script that can be run that will populate the database

            $ heroku run ./create_database.sh

Flask
-----
- Shell
    - Run a flask shell to load the flask application and be able to utilize the objects for debugging, testing, etc.
    
            $ flask shell

Tesseract
---------
Tesseract is an open source text recognition (OCR) engine used for parsing screenshots from the game for the village
tools.

https://github.com/tesseract-ocr/tessdoc/blob/master/Home.md

See /tesseract for details on how I trained tesseract to recognize the V&H font for improved accuracy.
