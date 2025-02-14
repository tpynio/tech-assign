# tech-assign
## Техническое задание
Техническое задание в [SPECIFICATION.md](./SPECIFICATION.md)

## Переменные окружения
TODO

## Разработка
1. В PyCharm устанавливаем virtualenv (Python3.13)
2. В Pycharm открываем терминал (он автоматически установит source) и устанавливаем pipenv
```shell
pip install pipenv
```
3. установка всех зависимостей
```shell
pipenv install
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
