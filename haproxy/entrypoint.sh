#!/bin/sh

echo "global
	maxconn 2048
	tune.ssl.default-dh-param 2048
defaults
	mode http
	option forwardfor
	option http-server-close
	stats enable
	stats uri $STATS_URI
	stats realm Haproxy\ Statistics
	stats auth $STATS_USER:$STATS_PASSWORD
frontend www-http
	bind :${HAPROXY_HTTP_BIND_PORT}
	reqadd X-Forwarded-Proto:\ http
	default_backend www-backend
	timeout client 30000
frontend www-https
	bind :$HAPROXY_HTTPS_BIND_PORT ssl crt $HAPROXY_PEM_PATH
	reqadd X-Forwarded-Proto:\ https
	default_backend www-backend
	timeout client 30000
backend www-backend
	redirect scheme https if !{ ssl_fc }
	server www-1 $BACKEND_HOST_A:$BACKEND_PORT check
	timeout connect 5000
	timeout check 5000
	timeout server 30000" > $HAPROXY_CONF &&

export PRIVATE_KEY="`echo $PRIVATE_KEY | sed 's/\"//g'`"
export CERTIFICATE="`echo $CERTIFICATE | sed 's/\"//g'`"

echo "$PRIVATE_KEY\n$CERTIFICATE" > $HAPROXY_PEM_PATH &&

export PRIVATE_KEY=
export CERTIFICATE=

/docker-entrypoint.sh haproxy -f $HAPROXY_CONF
