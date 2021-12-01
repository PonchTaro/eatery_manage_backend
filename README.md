## Description
* 名前の由来は、フランス語のMoNGe(食べる)と英語のMaNaGe(管理する)を掛けて、FastにMNGするアプリという意味を込めた。
* 飲食店を始める際に、客自身にモバイル端末で注文してもらうシステムが手軽に導入できると喜ぶ人もいるかと思った。
* 新しい店舗を始める際のスタッフを募集する手間の削減, 営業中の人件費の削減を目的とする。
* フロントエンドは[ここ](https://github.com/shigekato/eatery_manage_frontend)

## (エセ)ER図
![image](https://user-images.githubusercontent.com/31150623/144195308-db72baae-b38e-4960-adf8-4a6d3adf3762.png)
* https://docs.google.com/presentation/d/1WaU-hbif61SbpiykjSl37folaw7ukwc7WVLN4TJ2Lsk/edit#slide=id.g104f691ba8c_0_0

## 機能
#### 客
* テーブルに座ったらテーブルのQRコードを読み取る。
* 注文を開始できる。
* メニュー一覧から商品を選んで注文をしていく。
* 注文履歴が見れる。
* 離席する際に会計する。(未実装)paypayでやろうと最近思った。

#### 店
* 注文できる品物を登録する。
* 注文できる品物の種類を登録する(品物をグループ分けして表示するため)
* テーブルの情報を登録する。(椅子の数など)
* テーブルに紐づくQRコードの発行

## イメージ
![image](https://user-images.githubusercontent.com/31150623/142143710-36b5a78e-2c9b-43a7-9f41-c28f710301b2.png)

## Discussion
* 開発を始めてから愛着もなくやめてしまった。もう少しUX, UIも考えて作り込めば楽しんで開発にのめり込めたかもしれない。
* 「ひとつの店舗で飯を食うためにアプリをインストールするのは面倒」という発想を前提にしてwebアプリで開発しているが、これは正しいだろうか？

