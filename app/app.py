from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model_path = "../models/model.pkl"
model = pickle.load(open(model_path, 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET'])
def predict():
    return render_template('predict.html')

@app.route('/result', methods=['POST'])
def result():
    class_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    
    sepal_length = request.form['sepal_length']
    sepal_width = request.form['sepal_width']
    petal_length = request.form['petal_length']
    petal_width = request.form['petal_width']

    data = [sepal_length, sepal_width, petal_length, petal_width]
    data = [float(i) for i in data]
    prediction = model.predict([np.array(data)])

    iris_species = class_map.get(prediction[0], "Unknown species")

    message = f"The predicted species for the entered measurements is: {iris_species}"
    
    return render_template('result.html', message=message)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
