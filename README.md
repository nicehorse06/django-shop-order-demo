# Django shop order demo

### 初始化所有資料
* `python manage.py loaddata */fixtures/initial_*`

## 完成
* 加入訂單,訂單成立需檢查是否符合vip身份,並確認商品庫存數量(身份和庫存檢查限用decorator實作)

## todo
* UI 美化
    * 一些必要的提示文字，比如欄位目前沒有資料
    * 把input的說明塞到input裡面
* 刪除訂單(身份和庫存檢查限用decorator實作)
    * 備註:加入訂單時,若小於可購買量,前端需提示貨源不足 / 刪除訂單,庫存從0變回有值則提示商品到貨 
* 請設計一排程,根據訂單記錄算出各個館別的1.總銷售金額 2.總銷售數量 3.總訂單數量
    * 備註:輸出方式不限(ex: slack通知,email通知,生成csv,...)
* 使用docker佳
* 部署至雲端服務佳
* 單元測試

### todo中的todo
* django 匯出 csv
* redis、celery建制
* docker django hello world
* 單元測試hello world
* 部屬GCP