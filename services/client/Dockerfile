# pull official base image
FROM node:19

WORKDIR /app
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

RUN npm ci
COPY . /app

# start app
CMD ["npm", "run", "dev"]
