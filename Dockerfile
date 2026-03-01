FROM python:3.11-slim

LABEL maintainer="Syed Ali Turab"
LABEL description="PetCare Triage & Smart Booking Agent"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

ENV APP_ENV=production
ENV PORT=5002

CMD ["python", "backend/api_server.py"]
