# Django shop order demo

* 目前celery_app吃不到settings裡面的資料，暫時把redis的設定寫死到裡面
    * todo

## 相關指令
* 初始化product資料: `python manage.py loaddata */fixtures/initial_*`
* celery: `python shop_web/celery_app.py `
* 啟動redis:`redis-server`
* 啟動單元測試：`python manage.py test`


### todo中的todo
* docker django hello world
* 持續完成單元測試
* 部屬GCP
    * supervisor提供task和gunicorn服務
* css匯入問題 參照[https://stackoverflow.com/questions/6014663/django-static-file-not-found]
* task csv問題

### GCP
* git
* sudo apt install python3-pip
* pip install -r
* makemigrations
* migrate
* loaddata
* nginx
* redis
    * sudo apt-get install redis-server
* gunicorn
    * pip install 
    * `sudo gunicorn -w 4 -b 127.0.0.1:8080 shop_web.wsgi:application –reload –max-requests 1`
* supervisor
    * sudo apt install supervisor
```
directory=/var/www/django-shop-order-demo/shop_web/
command=sudo gunicorn -w 4 -b 127.0.0.1:8080 shop_web.wsgi:application –reload –max-requests 1
autostart=true
autorestart=true
stderr_logfile=/var/log/django-shop-order-demo.err.log
stdout_logfile=/var/log/django-shop-order-demo.out.log
```   

### Ref
* [Testing in Django](https://docs.djangoproject.com/en/2.2/topics/testing/)
* [Attempt to write a readonly database - Django w/ SELinux error](https://stackoverflow.com/questions/21054245/attempt-to-write-a-readonly-database-django-w-selinux-error)