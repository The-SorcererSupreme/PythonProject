FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0:8000", "run:app"]