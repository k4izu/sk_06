# sk_06

## 必読

Flaskアプリ`sk_app`のサーバを起動する際は`sk_06`がカレントディレクトリであることを確認したうえで、`python run.py`を実行してください。\
htmlでページを追加する際は、以下を適用してください。\
userの場合、`templates/base_user.html`\
adminの場合、`templates/base_admin.html`\
\
例）sample.htmlの場合
```
<!-- base.htmlの適用 -->
{% extends "base.html" %}

<!-- ページタイトルの設定 -->
{% block title %}タイトル{% endblock %}

<!-- メインコンテンツ -->
{% block content %}
    <h1>ページ見出し</h1>
{% endblock %}
```

## Flaskの環境
AnacondaのFlaskにて動かします。
\
開発は現状「C:\work\group\sk_06」で行っています。

# 必要なモジュール（Flask環境の作り方はnotionに記載）
### mediapipe関連
```
pip install mediapipe
conda install opencv
```
### flaskでCORS（Cross-Origin Resource Sharing）を有効にする
- pythonからjsへデータへデータを送る
 ```
pip install -U flask-cors
```
### DB関連（ORM適用まで）
-myswl-connector
```
pip install mysql-connector-python
```
-画像処理
```
pip install pillow
```

## メンバー

| メンバー名 | Name1      | Name2        |
| ----- | ---------- | ------------ |
| 海津     | k4izu | kaizu  |
| 門脇    | jmn04 | Yamato Kadowaki  |
| 草野 | ohs20562 |  |
| 坂口    | sacchier |              |
| 佐々木    | sasaki20571 |  |
| 谷    | tani-m1k |  |
| 飛田    | taka-0305  |  |
| 三谷    | mitani0928 |  |
