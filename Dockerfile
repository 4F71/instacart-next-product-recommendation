FROM python:3.10-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN sed -i 's/\r$//' run_app.sh


RUN chmod +x run_app.sh

EXPOSE 7860

CMD ["./run_app.sh"]