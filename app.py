import os
import pandas as pd
import numpy as np

from flask import Flask, render_template, request
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

app = Flask(__name__)

# =========================
# GLOBAL MODEL (SAFE LOAD)
# =========================
model = None


# =========================
# LOAD + TRAIN MODEL ON STARTUP
# =========================
def train_model():
    global model

    try:
        # Adjust path if needed
        file_path = "data01.csv"

        if not os.path.exists(file_path):
            print("ERROR: data01.csv not found in deployment")
            return

        df = pd.read_csv(file_path)

        df = df[['EF','Systolic blood pressure','gendera','Blood sodium','PCO2',
                 'Chloride','MCH','Bicarbonate','MCHC','MCV','Neutrophils',
                 'BMI','age','COPD','temperature','Urine output',
                 'Platelets','outcome']]

        # Fill missing values
        df.fillna(df.median(numeric_only=True), inplace=True)

        x = df.drop('outcome', axis=1)
        y = df['outcome']

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.3, random_state=42, stratify=y
        )

        model = LinearDiscriminantAnalysis()
        model.fit(x_train, y_train)

        print("Model trained successfully")

    except Exception as e:
        print("Error in training:", str(e))


# Train model once when app starts
train_model()


# =========================
# ROUTES
# =========================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/load', methods=["GET", "POST"])
def load_data():
    if request.method == "POST":
        data = request.files['data']
        df = pd.read_csv(data)
        msg = 'Data Loaded Successfully'
        return render_template('load.html', msg=msg)

    return render_template("load.html")


@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    if request.method == "POST":
        return render_template(
            'preprocess.html',
            msg='Data is already preprocessed at startup (Azure safe version)'
        )

    return render_template('preprocess.html')


@app.route('/model', methods=["GET", "POST"])
def model_page():
    if request.method == "POST":
        if model is None:
            return render_template("model.html", msg="Model not loaded")

        msg = "Model (LDA) is trained and ready"
        return render_template("model.html", msg=msg)

    return render_template("model.html")


@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if request.method == "POST":

        if model is None:
            return render_template("prediction.html", msg="Model not available")

        try:
            features = [
                float(request.form['EF']),
                float(request.form['Systolic blood pressure']),
                float(request.form['gendera']),
                float(request.form['Blood sodium']),
                float(request.form['PCO2']),
                float(request.form['Chloride']),
                float(request.form['MCH']),
                float(request.form['Bicarbonate']),
                float(request.form['MCHC']),
                float(request.form['MCV']),
                float(request.form['Neutrophils']),
                float(request.form['BMI']),
                float(request.form['age']),
                float(request.form['COPD']),
                float(request.form['temperature']),
                float(request.form['Urine output']),
                float(request.form['Platelets'])
            ]

            result = model.predict([features])[0]

            if result == 0:
                msg = "The patient life is Risky"
            else:
                msg = "The patient life is Less Risky"

            return render_template("prediction.html", msg=msg)

        except Exception as e:
            return render_template("prediction.html", msg=f"Error: {str(e)}")

    return render_template("prediction.html")


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False)