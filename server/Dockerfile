FROM node:slim

WORKDIR /srv

ENV PORT 5050

ADD app           /srv/app
ADD public        /srv/public
ADD server.js     server.js
ADD package.json  package.json

RUN npm install

ENTRYPOINT ["node"]
CMD ["server.js"]
