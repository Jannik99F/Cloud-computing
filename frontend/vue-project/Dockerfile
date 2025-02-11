# using node:22 with alpine linux as base image
FROM node:22-alpine AS dev

# create working directory
WORKDIR /app

# copy package.json and package-lock.json
COPY package*.json ./

# install dependencies
RUN npm install

# copy all files
COPY . .

# standard port for vite/vue is 5173, expose it
EXPOSE 5173

# run the dev server
CMD ["npm", "run", "dev"]