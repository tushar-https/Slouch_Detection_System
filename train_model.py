import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Path to the database file
DATABASE_FILE = 'sensorsData.db'

# Fetch data from the database
def fetch_data():
    conn = sqlite3.connect(DATABASE_FILE)
    query = "SELECT sensor_value, is_slouching FROM flex_sensor_data"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Preprocess data
def preprocess_data(data):
    X = data[['sensor_value']]  # Feature (sensor_value)
    y = data['is_slouching']    # Label (is_slouching)
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the model
def save_model(model, filename='slouch_detector.pkl'):
    joblib.dump(model, filename)
    print(f"Model saved as {filename}")

# Main function
if __name__ == "__main__":
    # Step 1: Fetch data
    data = fetch_data()
    
    # Step 2: Preprocess data
    X_train, X_test, y_train, y_test = preprocess_data(data)
    
    # Step 3: Train the model
    model = train_model(X_train, y_train)
    
    # Step 4: Evaluate the model
    evaluate_model(model, X_test, y_test)
    
    # Step 5: Save the trained model
    save_model(model)
