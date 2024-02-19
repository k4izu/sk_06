from sk_app.apps import app
from flask import render_template,Blueprint,request,redirect


users_login_view=Blueprint('users_login_view',__name__)

# パスの設定
user = "user/"

# ===== 空要素たち =====
# エラーメッセージ
err_msg={}
# 入力データ
login_form={}
signup_form={}
reset_form={}

# ==========================================================
#   ログイン                ("/")
# ==========================================================
@app.route("/")
def index():
    return render_template(user + "login.html",err_msg=err_msg,login_form=login_form)


# ==========================================================
#   ログイン確認             ("/login/check")
#   OK："/user" NO："login.html"
# ==========================================================
@app.route("/login/check", methods=["POST"])
def login_check():    
    # ===== データ受信
    login_form = request.form
    # ===== 入力項目TBL 
    vtbl = {
        'login_email':"メールアドレス",
        'login_pass':"パスワード"
    }
    # ===== 受信データの空白チェック
    flg = 0
    for key, value in login_form.items():
        #===== 未入力時のエラー処理
        if not value:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        #===== データが送られていない際の処理
        elif login_form[key] == None:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        else:
            #==== エラーメッセージの初期化
            err_msg[key] = ""
    # ===== 入力漏れが合った場合は再び"login.html"へ
    if flg != 0:
        return render_template(user + "login.html",err_msg=err_msg, login_form=login_form)
    else:
        return redirect("/user")


# ==========================================================
#   会員登録                ("/signup")
# ==========================================================
@app.route("/signup", methods=["GET"])
def signup():
    return render_template(user+"signup.html",err_msg=err_msg, signup_form=signup_form)


# ==========================================================
#   会員登録確認             ("/signup/check")
#   OK："/signup/comp" NO："signup.html"
# ==========================================================
@app.route("/signup/check", methods=["POST"])
def signup_check():
    # ===== データ受信
    signup_form = request.form
    # ===== 入力項目TBL
    vtbl = {
        'signup_name':"ユーザー名",
        'signup_email':"メールアドレス",
        'signup_pass':"パスワード",
        "signup_pass_check":"パスワード(確認用)"
    }
        # ===== 受信データの空白チェック
    flg = 0
    for key, value in signup_form.items():
        #===== 未入力時のエラー処理
        if not value:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        #===== データが送られていない際の処理
        elif signup_form[key] == None:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        else:
            #==== エラーメッセージの初期化
            err_msg[key] = ""
    # ===== 入力漏れが合った場合は再び"signup.html"へ
    if flg != 0:
        return render_template(user+"signup.html",err_msg=err_msg, signup_form=signup_form)
    # ===== 登録完了ページ"signup_comp.html"へ
    return render_template(user+"signup_comp.html",signup_form=signup_form)


# ==========================================================
#   パスワード再設定              ('/login/reset/password')
# ==========================================================
@app.route("/login/reset/password", methods=["get"])
def reset_password():
    return render_template(user+"reset_password.html",err_msg=err_msg,reset_form=reset_form)


# ==========================================================
#   パスワード再設定完了          ('/login/reset/password/comp')
# ==========================================================
@app.route("/login/reset/password/comp", methods=["get"])
def reset_password_comp():
    return render_template(user+"reset_password_comp.html",err_msg=err_msg,reset_form=reset_form)