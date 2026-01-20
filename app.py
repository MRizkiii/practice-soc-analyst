from flask import Flask, render_template
from parsing import log, is_valid_login_line, parsing
from main import generate_report

app = Flask(__name__)

@app.route("/")
def dashboard():
    fullData = []
    with open("auth.log", "r") as f:
        for x in f:
            if log(x) and is_valid_login_line(x):
                data = parsing(x)
                fullData.append(data)

    report = generate_report(fullData)

    return render_template(
        "dashboard.html",
        ipsort=report["ipsort"],
        usersort=report["usersort"],
        jamsort=report["jamsort"],
        alarms=report["alarms"]
    )

if __name__ == "__main__":
    app.run(debug=True)
