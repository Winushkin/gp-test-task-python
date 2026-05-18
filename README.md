# 📁 Проект: Device Statistics Service - Краткая сводка

## ⚡ TL;DR (самое важное)

**Что это?**
REST API сервис для сбора и анализа данных с устройств (x, y, z координаты).

**Как запустить?**
```bash
docker-compose up -d
# API доступна на http://localhost:8000
# Документация: http://localhost:8000/docs
```

**Как использовать?**
```bash
# Создать устройство
curl -X POST "http://localhost:8000/api/devices/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"sensor_1","name":"My Sensor"}'

# Добавить измерение
curl -X POST "http://localhost:8000/api/devices/sensor_1/measurements" \
  -H "Content-Type: application/json" \
  -d '{"x":10.5,"y":20.3,"z":-5.1}'

# Получить статистику
curl "http://localhost:8000/api/devices/sensor_1/statistics"
```

---

## 📂 Структура файлов и что где

```
📦 device-statistics/
│
├── 📄 README.md                 👈 НАЧНИ ОТСЮДА - полное описание проекта
├── 📄 SETUP.md                  👈 Инструкции по запуску и troubleshooting
├── 📄 ARCHITECTURE.md           👈 Описание архитектуры системы
├── 📄 LOAD_TESTING.md           👈 Как запустить нагрузочное тестирование
├── 📄 EXAMPLES.sh               👈 Примеры curl команд
│
├── 🐳 Dockerfile                ❌ Не трогай - Docker файл
├── 🐳 docker-compose.yml        ❌ Не трогай - запускает все контейнеры
├── 📄 requirements.txt          ❌ Не трогай - список зависимостей
├── 📄 .env.example              ❌ Не трогай - пример переменных окружения
├── 📄 .gitignore                ❌ Не трогай - что исключить из git
│
└── 📁 app/                      ✅ ОСНОВНОЙ КОД ПРИЛОЖЕНИЯ
    │
    ├── 📄 __init__.py           (пусто - нужно для Python)
    ├── 📄 main.py               👈 Начало приложения (FastAPI инициализация)
    ├── 📄 database.py           👈 Подключение к PostgreSQL
    ├── 📄 models.py             👈 Структура таблиц БД (User, Device, Measurement)
    ├── 📄 schemas.py            👈 Правила валидации данных (request/response)
    ├── 📄 crud.py               👈 Функции работы с БД (создание, получение, анализ)
    │
    └── 📁 routers/              👈 API endpoints (что доступно по HTTP)
        ├── 📄 __init__.py       (пусто)
        ├── 📄 devices.py        👈 API для устройств и их измерений
        └── 📄 users.py          👈 API для пользователей (опционально)

└── 📁 tests/                    ✅ ТЕСТИРОВАНИЕ
    ├── 📄 __init__.py           (пусто)
    └── 📄 locustfile.py         👈 Нагрузочное тестирование (Locust)
```

---

## 🔄 Как данные текут через систему

### 1️⃣ Создание устройства
```
Client HTTP request
    ↓
main.py (FastAPI инициализация)
    ↓
routers/devices.py (получить POST запрос)
    ↓
crud.py: create_device() (сохранить в БД)
    ↓
models.py: Device (структура таблицы)
    ↓
database.py (PostgreSQL)
    ↓
Ответ клиенту
```

### 2️⃣ Добавление измерения
```
Client HTTP request с {x, y, z}
    ↓
routers/devices.py: add_measurement()
    ↓
schemas.py: MeasurementCreate (проверить формат)
    ↓
crud.py: create_measurement() (сохранить)
    ↓
models.py: Measurement (в БД)
    ↓
Ответ
```

### 3️⃣ Получение статистики
```
Client запрос на статистику
    ↓
routers/devices.py: get_statistics()
    ↓
crud.py: get_device_statistics()
    ├─ Получить все измерения из БД (SELECT * FROM measurements)
    ├─ Разделить на x, y, z
    ├─ crud.py: calculate_statistics()
    │  ├─ min(values)
    │  ├─ max(values)
    │  ├─ len(values)
    │  ├─ sum(values)
    │  └─ median(values)
    └─ schemas.py: StatisticsResponse (отформатировать ответ)
    ↓
Ответ с {min, max, count, sum, median}
```

---

## 🎯 Ключевые компоненты

### models.py - Структура БД
```python
User (пользователь)
├─ id: int
├─ name: string
└─ email: string

Device (устройство)
├─ id: int
├─ device_id: string (уникальный ID)
├─ name: string
└─ user_id: int (опционально)

Measurement (измерение)
├─ id: int
├─ device_id: int
├─ x: float
├─ y: float
├─ z: float
└─ timestamp: datetime
```

### schemas.py - Валидация данных
Проверяет, что клиент отправляет правильный формат:
```python
MeasurementCreate = {"x": float, "y": float, "z": float}
DeviceCreate = {"device_id": string, "name": string, "user_id": optional int}
```

### crud.py - Бизнес-логика
- `create_device()` - создать устройство
- `create_measurement()` - добавить измерение
- `get_measurements_by_device()` - получить все измерения
- `calculate_statistics()` - вычислить min, max, sum, count, median
- `get_device_statistics()` - получить статистику устройства

### routers/devices.py - REST API
Определяет что доступно по HTTP:
```
POST   /api/devices/                     ← создать устройство
GET    /api/devices/                     ← список устройств
GET    /api/devices/{device_id}          ← информация об устройстве
DELETE /api/devices/{device_id}          ← удалить устройство

POST   /api/devices/{device_id}/measurements          ← добавить измерение
GET    /api/devices/{device_id}/measurements          ← список измерений
GET    /api/devices/{device_id}/statistics            ← статистика
```

---

## 🗄️ База данных

### Структура (Entity Relationship Diagram)

```
┌─────────────┐
│   Users     │
├─────────────┤         ┌──────────────┐
│ id (PK)     │────────→│  Devices     │
│ name        │  1    N ├──────────────┤      ┌──────────────────┐
│ email       │         │ id (PK)      │────→ │  Measurements    │
└─────────────┘         │ device_id    │  1 N ├──────────────────┤
                        │ name         │      │ id (PK)          │
                        │ user_id (FK) │      │ device_id (FK)   │
                        └──────────────┘      │ x, y, z (float)  │
                                              │ timestamp        │
                                              └──────────────────┘
```

### Примеры SQL (для понимания)

```sql
-- Создать устройство
INSERT INTO devices (device_id, name) VALUES ('sensor_001', 'My Sensor');

-- Добавить измерение
INSERT INTO measurements (device_id, x, y, z) VALUES (1, 10.5, 20.3, -5.1);

-- Получить все измерения устройства
SELECT * FROM measurements WHERE device_id = 1;

-- Статистика за период
SELECT 
  MIN(x) as min_x,
  MAX(x) as max_x,
  COUNT(*) as count,
  SUM(x) as sum_x
FROM measurements 
WHERE device_id = 1 AND timestamp BETWEEN '2024-01-01' AND '2024-12-31';
```

---

## 🌍 REST API endpoints

### Базовый URL
```
http://localhost:8000
```

### Dokumentasyon
```
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

### Основные endpoint'ы

#### Устройства
| Метод | Endpoint | Описание |
|-------|----------|---------|
| POST | `/api/devices/` | Создать устройство |
| GET | `/api/devices/` | Получить все устройства |
| GET | `/api/devices/{device_id}` | Информация об устройстве |
| DELETE | `/api/devices/{device_id}` | Удалить устройство |

#### Измерения
| Метод | Endpoint | Описание |
|-------|----------|---------|
| POST | `/api/devices/{device_id}/measurements` | Добавить измерение |
| GET | `/api/devices/{device_id}/measurements` | Получить измерения |
| GET | `/api/devices/{device_id}/measurements?start_time=...&end_time=...` | Измерения за период |

#### Статистика
| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/api/devices/{device_id}/statistics` | Статистика устройства |
| GET | `/api/devices/{device_id}/statistics?start_time=...&end_time=...` | Статистика за период |

#### Пользователи (опционально)
| Метод | Endpoint | Описание |
|-------|----------|---------|
| POST | `/api/users/` | Создать пользователя |
| GET | `/api/users/` | Список пользователей |
| GET | `/api/users/{user_id}/statistics` | Статистика по всем устройствам пользователя |

---

## 🧪 Тестирование

### Способ 1: Интерактивная документация
Просто откройте http://localhost:8000/docs и тестируйте там

### Способ 2: curl команды
```bash
# См. файл EXAMPLES.sh для всех примеров
bash EXAMPLES.sh  # Выполнить все примеры
```

### Способ 3: Нагрузочное тестирование
```bash
# Запустить Locust
locust -f tests/locustfile.py --host=http://localhost:8000

# Откройте http://localhost:8089
```

---

## 🐳 Docker команды

```bash
# Запустить всё
docker-compose up -d

# Остановить всё
docker-compose down

# Посмотреть логи
docker-compose logs -f api

# Перезагрузить API
docker-compose restart api

# Удалить всё включая данные
docker-compose down -v
```

---

## 📊 Пример использования (пошагово)

```bash
# 1. Запустить приложение
docker-compose up -d

# 2. Создать устройство
curl -X POST "http://localhost:8000/api/devices/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"temp_sensor","name":"Temperature Sensor"}'

# 3. Добавить несколько измерений
curl -X POST "http://localhost:8000/api/devices/temp_sensor/measurements" \
  -H "Content-Type: application/json" \
  -d '{"x":22.5,"y":45.0,"z":-10.2}'

curl -X POST "http://localhost:8000/api/devices/temp_sensor/measurements" \
  -H "Content-Type: application/json" \
  -d '{"x":23.1,"y":46.2,"z":-9.8}'

curl -X POST "http://localhost:8000/api/devices/temp_sensor/measurements" \
  -H "Content-Type: application/json" \
  -d '{"x":21.8,"y":44.5,"z":-11.1}'

# 4. Получить статистику
curl "http://localhost:8000/api/devices/temp_sensor/statistics" | python -m json.tool

# Ответ:
# {
#   "device_id": "temp_sensor",
#   "x_stats": {
#     "min_value": 21.8,
#     "max_value": 23.1,
#     "count": 3,
#     "sum": 67.4,
#     "median": 22.5
#   },
#   "y_stats": {...},
#   "z_stats": {...}
# }

# 5. Открыть веб-интерфейс
# http://localhost:8000/docs
```

---

## 📚 Документация проекта

| Файл | Для чего |
|------|----------|
| **README.md** | 📖 Полное описание проекта, функции, API |
| **SETUP.md** | 🚀 Как запустить, troubleshooting |
| **ARCHITECTURE.md** | 🏗️ Архитектура, дизайн, техническое обоснование |
| **LOAD_TESTING.md** | 📊 Нагрузочное тестирование с Locust |
| **EXAMPLES.sh** | 💡 Примеры curl команд для всех endpoint'ов |

---

## ✅ Что реализовано (требования ТЗ)

### ✅ Функциональные требования
- [x] Сбор статистики с устройства (x, y, z - float)
- [x] Анализ собранной статистики (min, max, count, sum, median)
- [x] Поддержка анализа за определенный период и за всё время
- [x] Добавление пользователей (опционально)
- [x] Получение анализа по пользователю (опционально)

### ✅ Нефункциональные требования
- [x] REST архитектура
- [x] FastAPI фреймворк
- [x] Сохранение данных в БД (PostgreSQL)
- [x] Docker контейнеризация
- [x] docker-compose для развёртывания
- [x] Нагрузочное тестирование (Locust)

### 🎁 Бонусы
- [x] Полная документация (README, ARCHITECTURE, SETUP, LOAD_TESTING)
- [x] Примеры использования (curl, Swagger UI)
- [x] Troubleshooting гайд
- [x] Примеры нагрузочного тестирования

---

## 🚀 Готово к использованию!

Проект полностью готов к:
1. ✅ Локальному использованию (Docker или Python)
2. ✅ Тестированию (Swagger UI, curl, Locust)
3. ✅ Production развёртыванию (Docker, Kubernetes и т.д.)
4. ✅ Расширению (модульная архитектура)

**Начни с:**
1. Прочитай README.md
2. Запусти `docker-compose up -d`
3. Открой http://localhost:8000/docs
4. Тестируй API через Swagger UI или curl