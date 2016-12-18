FROM willnorris/imageproxy

ENV PORT 6060
ENV CACHE_DIR         /srv/imageproxy

ADD white_list.txt    white_list.txt
ADD entrypoint.sh     entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
