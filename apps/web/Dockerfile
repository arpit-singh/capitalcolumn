FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
# We don't set API_URL at build time because SSR will fetch at runtime
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Expose port
EXPOSE 3000

# Start Astro Node server
ENV HOST=0.0.0.0
ENV PORT=3000

CMD ["node", "./dist/server/entry.mjs"]
