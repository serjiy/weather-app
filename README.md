# Weather App

Это приложение показывает погоду по городу.  
Берёт данные из Open-Meteo API и кэширует в Redis, чтобы не использовать API каждый раз.

## Что тут происходит

- FastAPI приложение
- Dockerized (есть Dockerfile)
- CI/CD на GitHub Actions:
  - ставит пакеты (install)
  - проверяет код (lint через pylint)
  - запускает тесты (pytest)
  - строит Docker-образ и пушит его в ghcr.io

Всё запускается автоматически при пуше в main.  
Lint и test работают параллельно для оптимизации.

## Почему ghcr.io

Образы пушатся в GitHub Container Registry (ghcr.io), а не в Docker Hub, потому что:
- не нужен отдельный аккаунт — работает через встроенный GITHUB_TOKEN
- бесплатно
- удобно смотреть, из какого коммита образ собран

## Как запустить локально

1. git clone https://github.com/serjiy/weather-app.git
2. cd weather-app
3. docker build -t weather-app .
4. docker run -p 8000:8000 weather-app

Открыть http://localhost:8000

## PS

- Параллельные джобы — lint и test запускаются одновременно
- Docker-образ тут: https://github.com/serjiy/weather-app/packages

Что было сделано:

Создал репозиторий на GitHub: https://github.com/serjiy/weather-app
Взял исходный проект https://github.com/AnastasiyaGapochkina01/wheather-app и перенёс его к себе.
Добавил Dockerfile — для запуска в контейнере.
Настроил GitHub Actions (это CI/CD) — файл .github/workflows/ci-cd.yml
Pipeline делает следующее:
install — ставит зависимости
lint — проверяет код на ошибки (лёгкая версия, чтобы не ругался на всё подряд)
test — запускает тесты (pytest проходит)
build — собирает Docker-образ и пушит его в ghcr.io (GitHub Container Registry)
Всё это запускается автоматически при пуше в main.




