#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask
import sk_app.views

#Flaskオブジェクトの生成
app = Flask(__name__)