from sk_app.apps import app
from flask import render_template,Blueprint

admin_view=Blueprint('admin_view',__name__,url_prefix='/admin')

# パスの設定
admin = "admin/"

#「/admin」へアクセスがあった場合に、「admin/index.html」を返す
@app.route("/admin")
def admin_index():
    return render_template(admin + "index.html")