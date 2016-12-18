#!/bin/sh

export WHITE_LIST=`awk -vORS=, '{ print $1 }' white_list.txt | sed 's/,,//g'`

/go/bin/imageproxy -addr 0.0.0.0:$PORT -cache $CACHE_DIR -whitelist $WHITE_LIST
