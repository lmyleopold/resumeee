FROM node:lts-alpine AS base

RUN npm i -g pnpm

FROM base AS dependencies
WORKDIR /resumeee-frontend
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

FROM base AS build
WORKDIR /resumeee-frontend
COPY . .
COPY --from=dependencies /resumeee-frontend/node_modules ./node_modules
RUN pnpm build
RUN pnpm prune --prod

FROM nginx:stable-alpine AS deploy

WORKDIR /resumeee-frontend
COPY --from=build /resumeee-frontend/dist /usr/share/nginx/html
COPY --from=build /resumeee-frontend/node_modules ./node_modules
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]