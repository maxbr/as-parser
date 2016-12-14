FROM centos:centos7

ENV BACKEND_HOST_A      127.0.0.1
ENV BACKEND_PORT        5050
ENV BACKEND_CACHE_TIME  20m
ENV BACKEND_CACHE_SIZE  64m
ENV BACKEND_CONF        /etc/varnish/user.vcl

RUN yum update -y && \
  yum install -y epel-release && \
  yum install -y varnish && \
  yum install -y libmhash-devel && \
  yum clean all

ADD entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

EXPOSE 6081
EXPOSE 6082

ENTRYPOINT ["./entrypoint.sh"]
