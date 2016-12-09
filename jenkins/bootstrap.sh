#!/bin/bash

URL=$1
USER=$2
PASS=$3

# install plugins
echo "installing masrk-passwords@2.9 plugin"
curl -X POST -d '<jenkins><install plugin="mask-passwords@2.9" /></jenkins>' -H 'Content-Type: text/xml' "https://${USER}:${PASS}@${URL}/pluginManager/installNecessaryPlugins"

# create template job for running producer containers in hyper
curl -X POST "https://${USER}:${PASS}@{URL}/createItem?name=Producer_Hyper_CMD_Template" --data-binary "@producer_hyper_template.xml" -H "Content-Type: text/xml"
