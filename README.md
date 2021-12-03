## 導入
* 飲食店での人件費削減のために、お客様が持っている携帯端末を用いて注文を取るモバイルオーダーシステムはしばしば存在する。
* 自社ブランドを重視する飲食チェーンなどは自社向けにアプリを発注するだろう。例えば、マクドナルドやスターバックスなどだ。
* しかし、ブランディングを重視せず、人件費削減のためにとりあえず手軽にモバイルオーダーを導入したい飲食店の経営者も少なからず存在するそうである(聞き取り調査の結果)。
* そこで、システム開発を委託しなくても必要なデータを入力すれば、簡単にモバイルオーダーが実現できるシステムを作ろうと考えた。

##### 追加の説明
* 名前の由来は、フランス語のMoNGe(食べる)と英語のMaNaGe(管理する)を掛けて、FastにMNGするアプリという意味を込めた。
* フロントエンドは[ここ](https://github.com/shigekato/eatery_manage_frontend)

## (エセ)ER図
![image](https://user-images.githubusercontent.com/31150623/144195308-db72baae-b38e-4960-adf8-4a6d3adf3762.png)
* [googleスライド](https://docs.google.com/presentation/d/1WaU-hbif61SbpiykjSl37folaw7ukwc7WVLN4TJ2Lsk/edit#slide=id.g104f691ba8c_0_0)(私用)
* [ソースコード](https://github.com/shigekato/FastMNG_backend/blob/master/src/eatery_app/models.py)

## 機能
#### 客
* テーブルに座ったらテーブルのQRコードを読み取る。
* 注文を開始できる。
* メニュー一覧から商品を選んで注文をしていく。
* 注文履歴が見れる。
* 離席する際に会計する。(未実装)paypayでやろうと最近思った。
![image](https://user-images.githubusercontent.com/31150623/144627175-4d55115b-9112-4c65-b7cf-587ee914fe30.png)


#### 店
* 注文できる品物を登録する。
* 注文できる品物の種類を登録する(品物をグループ分けして表示するため)
* テーブルの情報を登録する。(椅子の数など)
* テーブルに紐づくQRコードの発行
![image](https://user-images.githubusercontent.com/31150623/144625849-a8c65c9d-bf2d-4321-9795-1bb14f514ecf.png)
![image](https://user-images.githubusercontent.com/31150623/144202697-98ce2e15-3b35-474c-b175-c89dc5c24146.png)

## Discussion
* 開発を始めてから愛着もなくやめてしまった。もう少しUX, UIも考えて作り込めば楽しんで開発にのめり込めたかもしれない。
* 「ひとつの店舗で飯を食うためにアプリをインストールするのは面倒」という発想を前提にしてwebアプリで開発しているが、これは正しいだろうか？
* 既存の例が既に多数存在する。
    * [LINE ミニアプリ](https://line-marketplace.com/jp/ebook/mini-app/miniapp-start-guide/order?utm_source=google&utm_medium=cpc&utm_campaign=kwm_ma_search&gclid=Cj0KCQiA15yNBhDTARIsAGnwe0UKBnIdYaoQej3fPa22ijnkn-TaS4GAn_ZeIKjWUfK8C-opi0hNu_oaAnSIEALw_wcB)
    * [Retty Order](https://lp.self-order.retty.me/?utm_source=google&utm_source=google&utm_medium=cpc&utm_medium=cpc&utm_campaign=mo&utm_campaign=mo&gclid=Cj0KCQiA15yNBhDTARIsAGnwe0UY6Hypc_3z9Lsemj5LBp_iJB8eKn3tw5C1vFT8YWJZTBey0GowGsIaAv9fEALw_wcB)
    * [Tap & Order](https://tap-n-order.com/lp/lp-2021003/?gclid=Cj0KCQiA15yNBhDTARIsAGnwe0U56uWCJMPIYhzjmoc_zn1YX7vgDHGuNXbpvRgZJ2coXGtMd8dlTKgaAlRaEALw_wcB)
