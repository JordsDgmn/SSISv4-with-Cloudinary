# === CRASH TRACEPOINT: app.py top ===
print("=== TRACEPOINT: app.py module loaded ===")
from website import create_app
from flask import Flask



app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)