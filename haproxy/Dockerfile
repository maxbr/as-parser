FROM haproxy:1.7

ENV BACKEND_HOST_A            127.0.0.1
ENV BACKEND_PORT              6081

ENV STATS_URI                 /stats
ENV STATS_USER                user
ENV STATS_PASSWORD            password

ENV HAPROXY_CONF              /usr/local/etc/haproxy/haproxy.cfg
ENV HAPROXY_HTTP_BIND_PORT    80
ENV HAPROXY_HTTPS_BIND_PORT   443
ENV HAPROXY_PEM_PATH          /etc/ssl/private/domain.pem

ENV PRIVATE_KEY               key
ENV CERTIFICATE               certificate

ADD entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
RUN mkdir -p /run/haproxy /var/lib/haproxy /etc/ssl/private

ENTRYPOINT ["./entrypoint.sh"]
