Heroes and Villagers
====================

Code related to the game Villagers &amp; Heroes

Heroku
------
Heroku (www.heroku.com) is used for hosting the application.
- Create the application in Heroku

        $ heroku login
        $ heroku create villagers-and-heroes
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

- Database

    - Not in use yet
    - https://devcenter.heroku.com/articles/getting-started-with-python#provision-a-database
