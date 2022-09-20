# Сервис уведомлений
[Техзадание](https://www.craft.do/s/n6OVYFVUpq0o6L). Сервис разработан на 
django rest framework

## Установка и запуск
1. Склонировать репозиторий с Github:
````
git clone git@github.com:s3r3ga/sms_messages.git
````
2. Перейти в директорию проекта
````
cd .../sms_message/
````
3. Создать виртуальное окружение:
````
python -m venv venv
````
4. Активировать окружение:
````
source venv/Scripts/activate
````
5. Создать файл .evn и заполнить необходимые данные:
```
URL = 'https://probe.fbrq.cloud/v1/send/'
TOKEN = '<your token>'
```
6. Установка зависимостей:
```
pip install -r requirements.txt
```
7. Создать и применить миграции в БД:
```
python manage.py makemigrations
python manage.py migrate
```
8. Запустить сервер
```
python manage.py runserver
```

***
```http://127.0.0.1:8000/api/``` - api проекта
```http://127.0.0.1:8000/api/clients/``` - клиенты
```http://127.0.0.1:8000/api/mailings/``` - рассылки
```http://127.0.0.1:8000/api/mailings/fullinfo/``` - общая статистика по всем рассылкам
```http://127.0.0.1:8000/api/mailings/<pk>/info/``` - детальная статистика по конкретной рассылке
```http://127.0.0.1:8000/api/messages/``` - сообщения
***