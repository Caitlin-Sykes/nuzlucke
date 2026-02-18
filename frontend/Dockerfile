FROM node:25-alpine AS build
LABEL "author"="Cait"
LABEL "nuzlucke.frontend.version"="1.0.0A"
LABEL "nuzlucke.release-date"="2026-02-18"
LABEL "description"="This is the frontend for the Nuzlucke project. This is built using Svelte 5"

WORKDIR /frontend
ARG VITE_API_URL

COPY package*.json ./

RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]