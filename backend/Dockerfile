FROM python:3.11-slim

WORKDIR /kanban-pm

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "backend"]