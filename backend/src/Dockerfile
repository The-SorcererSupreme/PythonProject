FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the backend port
EXPOSE 8000

# Increase Gunicorn workers and timeout
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]