import os
from flask import Flask, request, render_template

app = Flask(__name__)

# =========================
# SAFE GLOBAL MODEL (DISABLED TRAINING)
# =========================
model = None


# =========================
# HOME
# =========================
@app.route('/')
def index():
    return "App is running successfully on Azure"


# =========================
# ABOUT
# =========================
@app.route('/about')
def about():
    return "About page working"


# =========================
# LOAD DATA (SAFE - NO FILE CRASH)
# =========================
@app.route('/load', methods=['GET', 'POST'])
def load():
    if request.method == 'POST':
        file = request.files.get('data')

        if file:
            return "File received successfully"
        else:
            return "No file uploaded"

    return "Upload endpoint ready"


# =========================
# PREPROCESS (REMOVED FILE DEPENDENCY)
# =========================
@app.route('/preprocess')
def preprocess():
    return "Preprocessing skipped (no dataset dependency)"


# =========================
# MODEL (SAFE)
# =========================
@app.route('/model')
def model_page():
    return "Model is disabled to avoid deployment errors"


# =========================
# PREDICTION (SAFE DUMMY RESPONSE)
# =========================
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        return "Prediction endpoint working (model disabled for safety)"
    return "Prediction page ready"


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
