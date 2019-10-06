# Django shop order demo

* 如果在makemigrations時會出錯，需把urls.py裡面的view引入註解掉再執行
    * todo 待解決
* 目前celery_app吃不到settings裡面的資料，暫時把redis的設定寫死到裡面
    * todo

### 初始化所有資料
* `python manage.py loaddata */fixtures/initial_*`
* celery: `python shop_web/celery_app.py `
* 啟動redis:`redis-server`

## todo
* UI 美化
    * 一些必要的提示文字，比如欄位目前沒有資料
    * 把input的說明塞到input裡面 
* 使用docker佳
* 部署至雲端服務佳
* 單元測試

### todo中的todo
* docker django hello world
* 單元測試hello world
* 部屬GCP