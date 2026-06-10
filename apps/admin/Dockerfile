FROM node:20-slim AS build

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

# Override .env — use empty API_URL so all requests go through nginx proxy
ENV VITE_API_URL=""
RUN npm run build

# --- Serve with nginx ---
FROM nginx:alpine

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
