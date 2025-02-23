# Stage 1: Build Angular App
# Use Node.js version 18 (compatible with Angular CLI)
FROM node:18 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install -g @angular/cli
RUN npm install


# Copy the rest of the application code
COPY . .

#CMD ["ng", "serve", "--host", "0.0.0.0"]
CMD ["ng", "serve"]