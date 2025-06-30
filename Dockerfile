# Dockerfile

# 1. base image
FROM python:3.11-slim

# 2. prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# 3. set working directory
WORKDIR /app

# 4. install system deps (if needed) & Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. copy project
COPY . .

# 6. expose the port FastAPI/Uvicorn will run on
EXPOSE 8000

# 7. default command
#    Render will set the PORT env var; fall back to 8000 if not set
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
