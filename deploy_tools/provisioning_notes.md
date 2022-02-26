Обеспечение работы нового сайта
===============================
## Небходимые пакеты
* nginx
* python3
* virtualenv + pip
* git

например, в Ubuntu:
    sudo apt install nginx python3.8-venv git

## Конфигурация виртуального узла Nginx

* см. nginx.template.conf
* замените SITENAME, напримаер, на superlist.com
* поместить в /etc/nginx/sites-available/SITENAME
* Создать ссылку sudo ln -s /etc/nginx/sites-available/SITENAME /etc/nginx/sites-enabled/SITENAME

## Служба Systemd
* см. gunicorn-systemd.template.service
* замените SITENAME, напримаер, на superlist.com
* поместить в /etc/systemd/system/gunicorn-SITENAME.service

## Структура папок
Если допустить, что есть учетная запись пользователя в /home/username

```
/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── venv
```
