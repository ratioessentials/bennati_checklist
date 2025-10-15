FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application
COPY . .

# Esponi porta per development/production
EXPOSE 5173

# Default command (può essere sovrascritto da docker-compose)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

