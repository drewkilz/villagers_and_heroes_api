#!/bin/bash
# This script will pull the latest code for the API, restart the service, then print the status and logs

# Change working directory to one level up
dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
cd $dir/../

# Update to the latest code
git pull origin master

# Restart the API service
sudo systemctl restart villagers_and_heroes_api

# Print the status to check and make sure it restarted
sudo systemctl status --lines=0 villagers_and_heroes_api

# Display the logs
sudo journalctl -f -u villagers_and_heroes_api
