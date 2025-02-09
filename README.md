# MTS

Структура проекта:

moviespider/
│   scrapy.cfg
│
├── moviespider/
│   ├── __init__.py
│   ├── items.py      <-- Определение моделей данных
│   ├── pipelines.py  <-- Обработка данных после парсинга
│   ├── middlewares.py
│   ├── settings.py
│   ├── spiders/      <-- Папка с пауком
│   │   ├── __init__.py
│   │   ├── movies_spider.py <-- Основной паук для парсинга фильмов
│   ├── result.csv  <-- Пример отработки моего парсера
