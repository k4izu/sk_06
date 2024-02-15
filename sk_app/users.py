from sk_app.apps import app
from flask import render_template,Blueprint

user_view=Blueprint('users_view',__name__,url_prefix='/user')

# パスの設定
user = "user/"

#「/user」へアクセスがあった場合に、「user/index.html」を返す
@app.route("/user")
def user_index():
    return render_template(user + "index.html")