FROM python:3.12-slim
WORKDIR /app
COPY server.py .
RUN useradd -m app && mkdir /app/data && chown app:app /app/data
USER app
EXPOSE 8000
CMD ["python", "server.py"]
