from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained pipeline model
with open('best_regression_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Mapping for categorical fields
delivery_method_map = {"Express": 0, "Overnight": 1, "Standard": 2}
traffic_map = {"Low": 0, "Medium": 1, "High": 2}
weather_map = {"Clear": 0, "Rainy": 1, "Snowy": 2}
priority_map = {"High": 0, "Medium": 1, "Low": 2}
transport_map = {"Air": 0, "Truck": 1, "Ship": 2}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Read form values
        distance = float(request.form['distance'])
        weight = float(request.form['weight'])
        delivery_method = request.form['delivery_method']
        traffic = request.form['traffic']
        weather = request.form['weather']
        priority = request.form['priority']
        transport = request.form['transport']

        # Map categories to numeric values
        data = np.array([[
            distance,
            weight,
            delivery_method_map.get(delivery_method, 0),
            traffic_map.get(traffic, 0),
            weather_map.get(weather, 0),
            priority_map.get(priority, 0),
            transport_map.get(transport, 0)
        ]])

        prediction = model.predict(data)[0]
        prediction = round(prediction, 2)

        return render_template('index.html', prediction_text=f"Estimated Delivery Time: {prediction} hours")

    except Exception as e:
        return render_template('index.html', error="Error occurred: " + str(e))

if __name__ == '__main__':
    app.run(debug=True)
