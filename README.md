# tech-assign
## Техническое задание
Техническое задание в [SPECIFICATION.md](./SPECIFICATION.md)

## Запуск
```shell
docker-compose up --build -d
```
## Разработка
1. В PyCharm устанавливаем virtualenv (Python3.13)

3. установка всех зависимостей
для работы приложения
```shell
pip install -r requirements.txt
```
для девелоперских штучек: линтеры/прекоммиты
```shell
pip install -r requirements.dev.txt
```

4. Устанавливаем хук для pre-commit (для прогона линтеров по коду до коммита в репозиторий)
```shell
pre-commit install
```
5. Кодим
6. .....
7. Прогоняем линтерами по наколбашенному (при необходимости)
```shell
pre-commit run --all-files
```
