# Django shop order demo

* python版本為3.6.8
* Django版本為2.2.8


## 功能說明:
* DB儲存商品列表和訂單紀錄
* 網頁顯示商品列表和訂單紀錄和前三受歡迎商品的表格
* 有訂單的建立和移除功能，會反應在商品的庫存
* 可輸入mail，會有celery task把館別的統計資料寄到該信箱
* 有基本的新增刪除提醒，包含庫存從0便有的商品到貨通知和庫存不足與vip限制的警告
* 有單元測試在app的test.py中，由於時間因素覆蓋率沒有很高，時間越往後，我會加上越多測試案例


## 開發使用流程
* 建立virtualenv
* 執行 `pip install -r requirement`
* 執行 `python manage.py makemigrations`
* 執行 `python manage.py migrate`
* 執行 `python manage.py loaddata */fixtures/initial_*` 初始化product資料
* 執行 `python manage.py runserver` 啟動測試 server
* 裝redis當作celery的broker，執行`python shop_web/celery_app.py `啟動celery
* 在settings填上發信的寄件人資訊
* 單元測試：`python manage.py test`
    * selenium需下載driver才能使用，參閱[Selenium Client Driver](https://seleniumhq.github.io/selenium/docs/api/py/)

### GCP佈署簡易流程
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
[supervisord]
directory=/var/www/django-shop-order-demo/shop_web/
command=sudo gunicorn -w 4 -b 127.0.0.1:8080 shop_web.wsgi:application –reload –max-requests 1
autostart=true
autorestart=true
stderr_logfile=/var/log/django-shop-order-demo.err.log
stdout_logfile=/var/log/django-shop-order-demo.out.log
```   

### GCP 重啟指令筆記
* nginx 自動重啟
* redis 自動重啟
* sudo supervisord -c /etc/supervisor/supervisord.conf
* sudo supervisord -c /etc/supervisor/celeryd.conf

### 參考資料
* [Testing in Django](https://docs.djangoproject.com/en/2.2/topics/testing/)
* [Attempt to write a readonly database - Django w/ SELinux error](https://stackoverflow.com/questions/21054245/attempt-to-write-a-readonly-database-django-w-selinux-error)
* [使用 supervisor 管理进程](http://liyangliang.me/posts/2015/06/using-supervisor/)
* [docker-django-celery-tutorial](https://github.com/twtrubiks/docker-django-celery-tutorial)
* [Django + Celery + Redis + Gmail 實現異步寄信](https://medium.com/@zoejoyuliao/django-celery-redis-gmail-%E5%AF%84%E4%BF%A1-375904d4224c)
* [查看 Linux TCP Port 被哪隻程式(Process)佔用](https://blog.longwin.com.tw/2013/12/linux-port-process-check-2013/)
