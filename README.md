# sk_06

## 必読

Flaskアプリ`sk_app`のサーバを起動する際は`sk_06`がカレントディレクトリであることを確認したうえで、`python run.py`を実行してください。\
htmlでページを追加する際は、`templates/base.html`を必ず適用するようにしてください。\
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

## envフォルダの作成
C:\work\group\sk_06にて現在envフォルダを用いて開発しています。（後々変わる可能性あり）
\
virtualenvのインストールなど詳細はnotionにて
\

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
