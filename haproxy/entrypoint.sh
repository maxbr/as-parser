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
	default_backend www-cache-backend
	timeout client 30000

frontend www-https
	bind :$HAPROXY_HTTPS_BIND_PORT ssl crt $HAPROXY_PEM_PATH
	reqadd X-Forwarded-Proto:\ https
	acl has_image_cache_uri path_beg /image_cache
	use_backend www-images if has_image_cache_uri
	default_backend www-cache-backend
	timeout client 30000

backend www-cache-backend
	redirect scheme https if !{ ssl_fc }
	server www-cache-backend-1 $BACKEND_HOST_A:$BACKEND_PORT check
	timeout connect 5000
	timeout check 5000
	timeout server 30000

backend www-images
	redirect scheme https if !{ ssl_fc }
	server www-images-1 $IMAGE_CACHE_HOST:$IMAGE_CACHE_PORT check
	timeout connect 5000
	timeout check 5000
	timeout server 30000

backend www-images-errors
  errorfile 503 /usr/local/etc/haproxy/400.http" > $HAPROXY_CONF &&

export PRIVATE_KEY="`echo $PRIVATE_KEY | sed 's/\"//g'`"
export CERTIFICATE="`echo $CERTIFICATE | sed 's/\"//g'`"

echo "$PRIVATE_KEY\n$CERTIFICATE" > $HAPROXY_PEM_PATH &&

export PRIVATE_KEY=
export CERTIFICATE=

/docker-entrypoint.sh haproxy -f $HAPROXY_CONF
