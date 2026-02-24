# pull official base image
FROM node:24

WORKDIR /app
COPY client/package.json /app/package.json
COPY client/package-lock.json /app/package-lock.json

RUN npm ci
COPY client /app

# start app
CMD ["npm", "run", "dev"]
