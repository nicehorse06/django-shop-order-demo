# Django shop order demo

* 目前celery_app吃不到settings裡面的資料，暫時把redis的設定寫死到裡面
    * todo

## 相關指令
* 初始化product資料: `python manage.py loaddata */fixtures/initial_*`
* celery: `python shop_web/celery_app.py `
* 啟動redis:`redis-server`
* 啟動單元測試：`python manage.py test`

## todo
* UI 美化
    * 一些必要的提示文字，比如欄位目前沒有資料
    * 把input的說明塞到input裡面 
* 使用docker佳
* 部署至雲端服務佳
* 單元測試

### todo中的todo
* docker django hello world
* 持續完成單元測試
* 部屬GCP

### Ref
* [Testing in Django](https://docs.djangoproject.com/en/2.2/topics/testing/)