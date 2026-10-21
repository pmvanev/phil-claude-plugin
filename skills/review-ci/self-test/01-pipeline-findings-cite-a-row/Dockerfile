FROM node:20.11.1-alpine@sha256:6798adbe7fa3bf6076eb36f0b7f660c71e4cedbbd1775e6aacaef432cddc82ed
WORKDIR /app
COPY . .
RUN npm ci --omit=dev
USER node
CMD ["node", "dist/server.js"]
