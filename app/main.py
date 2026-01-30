from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import redis.asyncio as redis
import os
import json
from typing import Optional
import logging

app = FastAPI(title="Weather API")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = None

class WeatherRequest(BaseModel):
    lat: float
    lon: float
    city: Optional[str] = None  # Для справки

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            "redis://redis:6379/0", 
            encoding="utf-8", 
            decode_responses=True
        )
    return redis_client

@app.on_event("startup")
async def startup():
    r = await get_redis()
    await r.ping()
    logger.info("Redis connected")

@app.get("/health")
async def health():
    r = await get_redis()
    await r.ping()
    return {"status": "healthy", "redis": "ok"}

@app.get("/weather")
async def get_weather(lat: float, lon: float):
    key = f"weather:{lat}:{lon}"
    r = await get_redis()
    
    cached = await r.get(key)
    if cached:
        logger.info("Cache hit")
        return json.loads(cached)
    
    logger.info("API call to Open-Meteo")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=auto"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Weather API error")
        data = resp.json()
    
    # Упрощаем ответ
    current = data.get("current", {})
    result = {
        "location": {"lat": lat, "lon": lon},
        "current": {
            "temperature_2m": current.get("temperature_2m"),
            "relative_humidity_2m": current.get("relative_humidity_2m"),
            "wind_speed_10m": current.get("wind_speed_10m"),
            "weather_code": current.get("weather_code"),
            "time": current.get("time")
        }
    }
    
    await r.setex(key, 600, json.dumps(result))  # 10 мин TTL
    logger.info("Data cached")
    return result

