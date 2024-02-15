from sk_app.apps import app
from flask import render_template,Blueprint

test_view=Blueprint('test_view',__name__,url_prefix='/test')

#「/admin」へアクセスがあった場合に、「admin/index.html」を返す
@app.route("/test")
def test():
    return "Hello, World!"