from sk_app.apps import app
from flask import render_template,Blueprint

admin_view=Blueprint('admin_view',__name__,url_prefix='/admin')

# パスの設定
admin = "admin/"

#「/admin」へアクセスがあった場合に、「admin/index.html」を返す
@app.route("/admin")
def admin_index():
    return render_template(admin + "index.html")

@app.route('/adminlogin')
def login():
    return render_template(admin + 'login.html')

@app.route('/userdata')
def udata():
    return render_template(admin + 'user_data.html')

@app.route('/userdevices')
def udevice():
    return render_template(admin + 'user_device.html')