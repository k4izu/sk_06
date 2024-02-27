from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,request,redirect,session

users_settings_view=Blueprint('users_settings_view',__name__)

# パスの設定
user = "user/"

# ===== 空要素たち =====
# エラーメッセージ
err_msg={}
# 入力データ


# ==========================================================
#   設定              ('/settings')
# ==========================================================
@app.route("/settings", methods=["get"])
def settings():
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    return render_template(user+"settings.html",user_data=user_data)


# ==========================================================
#   ログアウト                  ('/logout')
# ==========================================================
@app.route("/logout", methods=["get"])
def logout():
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    # ===== session削除
    session.pop('user_sess',None)
    return redirect('/')


# ==========================================================
#   アカウント削除確認              ('/settings/checkdel')
# ==========================================================
@app.route("/settings/checkdel", methods=["get"])
def settings_checkdel():
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    return render_template(user+"settings_checkdel.html",user_data=user_data)


# ==========================================================
#   アカウント削除              ('/settings/delete')
# ==========================================================
@app.route("/settings/delete", methods=["get"])
def settings_delete():
    return redirect('/login')
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    