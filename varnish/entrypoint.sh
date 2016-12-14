#!/bin/sh

echo "vcl 4.0;
backend default {
  .host = \"$BACKEND_HOST_A\";
  .port = \"$BACKEND_PORT\";
}
sub vcl_backend_response {
  set beresp.ttl = $BACKEND_CACHE_TIME;
}" > $BACKEND_CONF

varnishd -F -a :6081 -T localhost:6082 -f $BACKEND_CONF -S /etc/varnish/secret -s malloc,$BACKEND_CACHE_SIZE
