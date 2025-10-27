FROM python:3.12.6-slim
WORKDIR /app
COPY .. .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
LABEL authors="intarsboldans"
ENV PYTHONUNBUFFERED=1
CMD ["python", "app.py"]