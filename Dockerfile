# Образ Python
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Зависимости
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Порт, на котором работает FastAPI
EXPOSE 8000

# Команда запуска (uvicorn из requirements.txt)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]