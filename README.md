Villagers and Heroes API
========================

Code related to the game Villagers &amp; Heroes

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

Digital Ocean (Deployment)
--------------------------
The API is currently deployed on Digital Ocean.

Original deployment was done via:
    
    # SSH into the droplet on Digital Ocean
    ssh -i /Users/drewkilz/.ssh/id_rsa_do root@159.65.108.26
    
    # Add a user to run the applications
    adduser vnh
    
    # Make the user a superuser
    usermod -aG sudo vnh
    
    # Allow OpenSSH through the Firewall
    ufw allow OpenSSH
    ufw enable
    
    # Switch to the vnh user
    su vnh
    
    # install nginx and python - had to do one at a time as there were errors when trying to install all at once
    sudo apt update
    sudo apt install nginx
    sudo apt install python3-pip
    sudo apt install python3-dev
    sudo apt install build-essential
    sudo apt install libssl-dev
    sudo apt install libffi-dev
    sudo apt install python3-setuptools
    sudo apt install python3-venv
    sudo apt install libsm6 libxext6 libxrender-dev
    sudo apt autoremove
    
    # Enable HTTPS and HTTPS traffic
    sudo ufw allow 'Nginx Full'
    
    # Change to home directory
    cd ~

    # git clone our repo
    git clone https://github.com/drewkilz/villagers_and_heroes_api.git
    
    # Create a virtual environment and activate it
    python3.6 -m venv venv
    source venv/bin/activate
    
    # Install requirements
    pip install wheel
    pip install -r requirements.txt
    
    # Create the database
    ./create_database.sh
    
    # Create automatic startup of the API
    sudo vi /etc/systemd/system/villagers_and_heroes_api.service
    
        [Unit]
        Description=Gunicorn instance to serve Villagers and Heroes API
        After=network.target
    
        [Service]
        User=vnh
        Group=www-data
        WorkingDirectory=/home/vnh/villagers_and_heroes_api
        Environment="PATH=/home/vnh/villagers_and_heroes_api/venv/bin"
        Environment="FLASK_CONFIGURATION=production"
        Environment="FLASK_ENV=production"
        Environment="JSONIFY_PRETTYPRINT_REGULAR=True"
        Environment="SECRET_KEY=..."    # Insert the secret key in ...
        Environment="CORS_ORIGIN=['https://www.vnh.thespottedlynx.com', 'https://vnh.thespottedlynx.com']"
        ExecStart=/home/vnh/villagers_and_heroes_api/venv/bin/gunicorn --workers 3 --bind unix:villagers_and_heroes_api.sock -m 007 villagers_and_heroes:app
    
        [Install]
        WantedBy=multi-user.target
    
    # Start and enable the service, then check its status
    sudo systemctl start villagers_and_heroes_api
    sudo systemctl enable villagers_and_heroes_api
    sudo systemctl status villagers_and_heroes_api
    
    # Configure nginx to proxy requests
    sudo vi /etc/nginx/sites-available/villagers_and_heroes
        map $http_origin $cors_origin_header {
            default "";
            "http://159.65.108.26" "$http_origin";
            "http://vnh.thespottedlynx.com" "$http_origin";
            "http://www.vnh.thespottedlynx.com" "$http_origin";
        }
        
        map $http_origin $cors_cred {
            default "";
            "http://159.65.108.26" "true";
            "http://vnh.thespottedlynx.com" "true";
            "http://www.vnh.thespottedlynx.com" "true";
        }

        server {
            listen 80;
            server_name vnh.thespottedlynx.com www.vnh.thespottedlynx.com 159.65.108.26;
        
            add_header Access-Control-Allow-Origin $cors_origin_header always;
            add_header Access-Control-Allow-Credentials $cors_cred;
            add_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS, HEAD";
            add_header "Access-Control-Allow-Headers" "Authorization, Origin, X-Requested-With, Content-Type, Accept";
    
            location /api {
                include proxy_params;
                proxy_pass http://unix:/home/vnh/villagers_and_heroes_api/villagers_and_heroes_api.sock;
            }
        }
    
    sudo ln -s /etc/nginx/sites-available/villagers_and_heroes /etc/nginx/sites-enabled
    
    # Since we added server names, uncomment server_names_hash_bucket_size directive to avoid collisions
    sudo vi /etc/nginx/nginx.conf
    
    sudo nginx -t
    sudo systemctl restart nginx
    
    # Add HTTPS
    sudo add-apt-repository ppa:certbot/certbot
    sudo apt install python-certbot-nginx
    sudo certbot --nginx -d vnh.thespottedlynx.com -d www.vnh.thespottedlynx.com
        # option 2 - redirect
    
    # nginx will have been updated to redirect traffic over SSL, but need to add CORS info in
    sudo vi /etc/nginx/sites-available/villagers_and_heroes
        map $http_origin $cors_origin_header {
            default "";
            "https://vnh.thespottedlynx.com" "$http_origin";
            "https://www.vnh.thespottedlynx.com" "$http_origin";
        }
        
        map $http_origin $cors_cred {
            default "";
            "https://vnh.thespottedlynx.com" "true";
            "https://www.vnh.thespottedlynx.com" "true";
        }
        
        server {
            server_name vnh.thespottedlynx.com www.vnh.thespottedlynx.com;
        
            add_header Access-Control-Allow-Origin $cors_origin_header always;
            add_header Access-Control-Allow-Credentials $cors_cred;
            add_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS, HEAD";
            add_header "Access-Control-Allow-Headers" "Authorization, Origin, X-Requested-With, Content-Type, Accept";
        
            location /api {
                include proxy_params;
                proxy_pass http://unix:/home/vnh/villagers_and_heroes_api/villagers_and_heroes_api.sock;
            }
        
            listen 443 ssl; # managed by Certbot
            ssl_certificate /etc/letsencrypt/live/vnh.thespottedlynx.com/fullchain.pem; # managed by Certbot
            ssl_certificate_key /etc/letsencrypt/live/vnh.thespottedlynx.com/privkey.pem; # managed by Certbot
            include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
            ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
        }
    
        server {
            if ($host = www.vnh.thespottedlynx.com) {
                return 301 https://$host$request_uri;
            } # managed by Certbot
        
        
            if ($host = vnh.thespottedlynx.com) {
                return 301 https://$host$request_uri;
            } # managed by Certbot
        
        
            listen 80;
            server_name vnh.thespottedlynx.com www.vnh.thespottedlynx.com;
            return 404; # managed by Certbot
        }
       
       # Set up git to not ask for password when updating
       git config --global credential.helper store
       git pull origin master

Useful commands on the server:
    
    # Log files
    sudo less /var/log/nginx/error.log: checks the Nginx error logs.
    sudo less /var/log/nginx/access.log: checks the Nginx access logs.
    sudo journalctl -f -u nginx: checks the Nginx process logs.
    sudo journalctl -f -u villagers_and_heroes_api: checks your Flask app’s Gunicorn logs.
    
    # Reboot the machine
    sudo reboot
    
    # systemd commands
    sudo systemctl daemon-reload
    sudo systemctl restart villagers_and_heroes_api

    # nginx commands
    sudo systemctl stop nginx
    sudo systemctl start nginx
    sudo systemctl restart nginx
    sudo systemctl reload nginx  # Reloads without dropping connections - useful for configuration changes, for example
    sudo systemctl disable nginx  # To disable automatic startup when server boots
    sudo systemctl enable nginx  # Re-enable automatic startup
    
    # nginx files
    /var/www/html: The actual web content, which by default only consists of the default Nginx page you saw earlier, is served out of the /var/www/html directory. This can be changed by altering Nginx configuration files.
    /etc/nginx: The Nginx configuration directory. All of the Nginx configuration files reside here.
    /etc/nginx/nginx.conf: The main Nginx configuration file. This can be modified to make changes to the Nginx global configuration.
    /etc/nginx/sites-available/: The directory where per-site server blocks can be stored. Nginx will not use the configuration files found in this directory unless they are linked to the sites-enabled directory. Typically, all server block configuration is done in this directory, and then enabled by linking to the other directory.
    /etc/nginx/sites-enabled/: The directory where enabled per-site server blocks are stored. Typically, these are created by linking to configuration files found in the sites-available directory.
    /etc/nginx/snippets: This directory contains configuration fragments that can be included elsewhere in the Nginx configuration. Potentially repeatable configuration segments are good candidates for refactoring into snippets.
    /var/log/nginx/access.log: Every request to your web server is recorded in this log file unless Nginx is configured to do otherwise.
    /var/log/nginx/error.log: Any Nginx errors will be recorded in this log.

    # Certificate information
    - Congratulations! Your certificate and chain have been saved at:
    /etc/letsencrypt/live/vnh.thespottedlynx.com/fullchain.pem
    
    Your key file has been saved at:
    /etc/letsencrypt/live/vnh.thespottedlynx.com/privkey.pem
    
    Your cert will expire on 2020-10-19. To obtain a new or tweaked
    version of this certificate in the future, simply run certbot again
    with the "certonly" option. To non-interactively renew *all* of
    your certificates, run "certbot renew"
    
    # Delete a certificate
    $ sudo certbot delete

When a change is made, to update the server:

    ./bin/update.sh
