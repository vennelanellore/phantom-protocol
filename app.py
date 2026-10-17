import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

FLAG = os.environ.get("FLAG")
if not FLAG:
    raise RuntimeError("FLAG environment variable is not configured.")

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>The Phantom Protocol</title>
    </head>
    <body>
        <h1>The Phantom Protocol</h1>
        <p>Welcome to the internal API portal.</p>
        <p>Documentation status: incomplete.</p>
        <p>System notice: Legacy services may still be active.</p>
        <p>Hint: Not every service is documented on this page.</p>
    </body>
    </html>
    """


@app.route("/robots.txt")
def robots():
    return """
User-agent: *
Disallow: /api/
Disallow: /archive/
"""


@app.route("/api/profile")
def profile():
    user = request.args.get("user", "guest")

    return jsonify({
        "user": user,
        "role": "guest",
        "status": "active"
    })


@app.route("/api/status")
def status():
    return jsonify({
        "service": "Legacy Archive",
        "status": "online",
        "documentation": "restricted",
        "notice": "An older archive service may still be in use."
    })


@app.route("/archive/")
def archive_home():
    return jsonify({
        "service": "Legacy Archive",
        "message": "Authentication required."
    })


@app.route("/archive/report")
def archive_report():
    role = request.headers.get("X-Role", "guest")

    if role != "admin":
        return jsonify({
            "error": "Access denied",
            "message": "Insufficient privileges"
        }), 403

    return jsonify({
        "report": "Archived internal report",
        "flag": FLAG
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
