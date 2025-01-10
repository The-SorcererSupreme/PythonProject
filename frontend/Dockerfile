# Use the official Node.js image
FROM node:alpine

# Set the working directory to /usr/src/app in the container
WORKDIR /usr/src/app

# Copy the local frontend code into the container
COPY . /usr/src/app

# Install project dependencies
RUN npm install

# Install Angular CLI globally
RUN npm install -g @angular/cli

# Expose the Angular development server port
EXPOSE 4200

# Run Angular development server (this binds to 0.0.0.0 to be accessible from outside the container)
CMD ["ng", "serve", "--host", "0.0.0.0"]
