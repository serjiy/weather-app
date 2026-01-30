# Weather API Service
Сервис для получения текущей погоды по названию города с кэшированием в Redis. Использует бесплатный Open-Meteo API (без регистрации и ключей).

## Требования
- python3.12+
- redis7+

## Локальная установка
1) Склонировать репозиторий
```bash
git clone git@github.com:AnastasiyaGapochkina01/wheather-app.git
cd wheather-app
```
2) Установить redis
```bash
sudo apt install redis-server
```
3) Установить зависимости
```bash
pip install -r app/requirements.txt
```
4) Запустить
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Проверка
```bash
curl http://localhost:8000/health

curl "http://localhost:8000/weather?lat=55.7558&lon=37.6173"
```
Пример ответа
```json
{
  "location": {
    "name": "Москва",
    "lat": 55.7558,
    "lon": 37.6173,
    "country": "Russia"
  },
  "current": {
    "temperature_2m": -5.2,
    "relative_humidity_2m": 78,
    "wind_speed_10m": 3.5,
    "weather_code": 3,
    "time": "2026-01-28T06:00"
  }
}
```

Swagger UI
```bash
curl http://localhost:8000/docs
```
