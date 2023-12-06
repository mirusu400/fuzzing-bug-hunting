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
                return render_template("admin.html", data="Wrong!")

        return render_template("admin.html", data="Fill the input box", pre=1)
    return render_template("admin.html")


@app.route("/report", methods=["GET"])
def report():
    # Get param parametert
    param = request.args.get("param", "")
    # Return report.html with param
    if not param:
        return render_template("report.html")
    template = (
        """
        <html>
            <head>
                <title>Report</title>
            </head>
            <body>
                <h1>Report</h1>
                <p>Report: %s</p>
                <p> Your report has been sent to admin. </p>
            </body>
        </html>
    """
        % param
    )
    return template


@app.route("/memo")
def memo():
    global memo_text
    text = request.args.get("memo", "")
    memo_text += text + "\n"
    return render_template("memo.html", memo=memo_text)


@app.route("/tomcat")
def tomcat():
    return render_template("tomcat.html")


@app.route("/apache")
def apache():
    return render_template("tomcat.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
