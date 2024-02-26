from sk_app.apps import app
from flask import render_template,Blueprint,request,redirect,session
import mysql.connector
from datetime import timedelta

# ====================================================
# ===== sessionチェック    
# ===== 正：userの名前,パスワード 誤："FALSE"
# ====================================================
def session_check():
    user_session={}
    # === session存在チェック、無い場合は/loginへ
    if "user_sess" in session:
        user_session=session["user_sess"]
        # === 必要なデータのみ抽出
        res={
            "user_id":user_session["id"],
            "user_name":user_session["name"]
            # "user_email":user_session["email"]
        }
    # === 存在しない場合はログインページへ
    else:
        res="FALSE"
    return res