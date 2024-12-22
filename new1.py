from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def get_db_connection():
    conn = sqlite3.connect('sensorsData.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS flex_sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sensor_value NUMERIC,
            is_slouching BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

# Call this function once to initialize the database
init_db()

# Dictionary to store the latest flex sensor value and slouching status
sensor_data = {
    "sensor_value": None,
    "is_slouching": None
}

# Route to accept flex sensor data
@app.route('/update_sensor', methods=['POST'])
def update_sensor():
    global sensor_data
    try:
        # Get sensor value and optional is_slouching flag from the request
        sensor_value = request.json.get('sensor_value')
        is_slouching = request.json.get('is_slouching')  # Optional, default is None

        if sensor_value is not None:
            sensor_data["sensor_value"] = sensor_value
            sensor_data["is_slouching"] = is_slouching
            
            # Insert the sensor value and slouching status into the database
            conn = get_db_connection()
            conn.execute('INSERT INTO flex_sensor_data (sensor_value, is_slouching) VALUES (?, ?)', 
                         (sensor_value, is_slouching))
            conn.commit()
            conn.close()
            
            return jsonify({"status": "success", "message": "Sensor value updated"}), 200
        else:
            return jsonify({"status": "error", "message": "Missing sensor_value"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to send the latest sensor data to the frontend
@app.route('/get_sensor', methods=['GET'])
def get_sensor():
    global sensor_data
    return jsonify(sensor_data), 200

# Route to display sensor data on a webpage
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch all logged sensor data
@app.route('/get_all_sensor_data', methods=['GET'])
def get_all_sensor_data():
    conn = get_db_connection()
    sensor_data = conn.execute('SELECT * FROM flex_sensor_data ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in sensor_data]), 200

# Route to fetch only slouching data for analysis or frontend display
@app.route('/get_slouching_data', methods=['GET'])
def get_slouching_data():
    conn = get_db_connection()
    slouching_data = conn.execute('SELECT * FROM flex_sensor_data WHERE is_slouching = 1 ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in slouching_data]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
