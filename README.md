#  Device Statistics Service


**Что это?**
REST API сервис для сбора и анализа данных с устройств (x, y, z координаты).

**Как запустить?**
```bash
    cp env.example .env
	docker compose --env-file .env up --build

# API доступна на http://localhost:8000/api
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
device-statistics/
│
├──  Dockerfile                
├──  docker-compose.yml        
├──  requirements.txt          
├──  .env.example              
├──  .gitignore               
│
└──  app/                      
    │
    ├──  main.py              Точка входа в приложение
    ├──  database.py          Подключение к БД
    ├──  models.py            Модели таблиц БД
    ├──  schemas.py           Pydantic схемы
    ├──  crud.py              Репозиторий базы
    │
    └──  routers/              API ручки 
        ├──  devices.py        API для устройств
        ├──  measurments.py    API для измерений
        └──  users.py          API для пользователей

└── tests/                     Нагрузочное тестирование
    └── locustfile.py         
```


## Тестирование

### Способ 1: Интерактивная документация
Просто откройте http://localhost:8000/docs и тестируйте там


### Способ 2: Нагрузочное тестирование
```bash
# Запустить Locust
locust -f tests/locustfile.py --host=http://localhost:8000

# Откройте http://localhost:8089

# Введите параметры тестирования
# Number of users - Максимальное кол-во пользователей
# Ramp up - кол-во прибавляющихся пользователей в сек.
```

#### Итоги нагрузочного тестирования:
при Number of users = 100 и Ramp up = 10, сервер переодически не справляется и разрывает соединение.
При пиковой нагрузке это происходит примерно 2 раза из 12
