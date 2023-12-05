import os
from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "user")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD", "pass")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "secret_db")
mysql = MySQL(app)

memo_text = ""


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        uid = request.form.get("uid", "")
        upw = request.form.get("upw", "")
        if uid and upw:
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT * FROM users WHERE uid='{uid}' and upw='{upw}';")
            data = cur.fetchall()
            if data:
                return render_template("user.html", data=data)

            else:
                return render_template("index.html", data="Wrong!")

        return render_template("index.html", data="Fill the input box", pre=1)
    return render_template("index.html")


@app.route("/memo")
def memo():
    global memo_text
    text = request.args.get("memo", "")
    memo_text += text + "\n"
    return render_template("memo.html", memo=memo_text)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
