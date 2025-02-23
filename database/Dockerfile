# Use the official PostgreSQL image as the base
FROM postgres:13

# Set environment variables for PostgreSQL (these can be overridden by docker-compose)
ENV POSTGRES_DB=codepilot
ENV POSTGRES_USER=datawizard
ENV POSTGRES_PASSWORD=#zHGmK$dO*e$0cugeugcnKi$P18BuA2U

# Copy initialization scripts (if any)
COPY init-scripts/ /docker-entrypoint-initdb.d/

# Ensure proper permissions
RUN chmod -R 755 /docker-entrypoint-initdb.d/

# Expose PostgreSQL default port
EXPOSE 5432