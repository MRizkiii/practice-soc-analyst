"""
SSH Auth Log Analyzer - Flask Web Application

Provides a web dashboard for SSH log security analysis.
"""

from flask import Flask, render_template, jsonify
from parsing import log, is_valid_login_line, parsing
from main import generate_report, load_log_file

app = Flask(__name__)


@app.route("/")
def dashboard():
    """Main dashboard view."""
    fullData = load_log_file()
    report = generate_report(fullData)
    
    return render_template(
        "dashboard.html",
        ipsort=report["ipsort"],
        usersort=report["usersort"],
        jamsort=report["jamsort"],
        alarms=report["alarms"],
        correlations=report.get("correlations", []),
        summary=report.get("summary", {}),
    )


@app.route("/api/report")
def api_report():
    """JSON API endpoint for report data."""
    fullData = load_log_file()
    report = generate_report(fullData)
    
    # Convert to JSON-serializable format
    return jsonify({
        "ipsort": report["ipsort"][:50],
        "usersort": report["usersort"][:50],
        "jamsort": report["jamsort"],
        "alarms": report["alarms"],
        "correlations": report.get("correlations", []),
        "summary": report.get("summary", {}),
    })


if __name__ == "__main__":
    app.run(debug=True)
