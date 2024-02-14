from sk_app.apps import app
from flask import render_template

# パスの設定
user = "user/"
admin = "admin/"

#「/user」へアクセスがあった場合に、「user/index.html」を返す
@app.route("/user")
def user_index():
    return render_template(user + "index.html")

#「/admin」へアクセスがあった場合に、「admin/index.html」を返す
@app.route("/admin")
def admin_index():
    return render_template(admin + "index.html")


#「/test」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/test")
def test():
    return "Hello, World!"