from flask import Flask, request, jsonify,render_template
import csv
import os

app = Flask(__name__)

# Filepath for the CSV file
CSV_FILE = 'sensor_data.csv'

# Ensure the CSV file exists and has the correct headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['SensorValue', 'Label'])  # Header row

# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/logdata', methods=['GET'])
def log_data():
    # Extract query parameters
    sensor_value = request.args.get('sensor_value')
    label = request.args.get('label')

    # Ensure parameters are not None
    if sensor_value and label:
        # Append the data to the CSV file
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([sensor_value, label])  # Write data row

        print(f"Logged: SensorValue={sensor_value}, Label={label}")
        return jsonify({"message": f"Logged: SensorValue={sensor_value}, Label={label}"})
    else:
        return jsonify({"error": "Missing sensor_value or label"}), 400


@app.route('/slouch-detected', methods=['GET'])
def slouch_detected():
    sensor_value = request.args.get('sensor_value')

    if sensor_value:
        # Handle slouch detected logic here
        print(f"Slouch Detected! Sensor Value: {sensor_value}")

        # Notify user via console, email, or any other method
        # Example: Use print or a notification service
        return jsonify({"message": f"Slouch detected! Sensor Value: {sensor_value}"})
    else:
        return jsonify({"error": "Missing sensor_value"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
