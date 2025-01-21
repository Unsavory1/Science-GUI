from flask import Flask, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import cv2 as cv
import random
import time
import threading

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Sensor data generation (similar to your previous Python code)
def generate_sensor_data():
    while True:
        # Generate random data for sensors
        data = {
            'ze03': {'co': round(random.uniform(0, 10), 2)},
            'gps': {'lat': 5, 'lon': 6},
            'flurometer': {'cur': round(random.uniform(0, 5), 2), 'res': round(random.uniform(10, 1000), 2)},
            'bme688': {'temperature': round(random.uniform(20, 30), 2), 'pressure': round(random.uniform(1000, 1100), 2),
                       'humidity': round(random.uniform(30, 80), 2), 'altitude': round(random.uniform(0, 500), 2)},
            'mq4': {'methane': round(random.uniform(200, 1000), 2)},
            'sgp30': {'tvoc': round(random.uniform(0, 50), 2), 'co2': round(random.uniform(300, 500), 2)},
            'soil_probe': {'temperature': round(random.uniform(10, 30), 2), 'moisture': round(random.uniform(0, 100), 2),
                           'ph_value': round(random.uniform(5.5, 7.5), 2)},
            'as726x': {'s1': round(random.uniform(0, 4000), 2), 's2': round(random.uniform(0, 4000), 2),
                       's3': round(random.uniform(0, 4000), 2), 's4': round(random.uniform(0, 4000), 2),
                       's5': round(random.uniform(0, 4000), 2), 's6': round(random.uniform(0, 4000), 2)},
            'tsl2591': {'RadiationIntesity': round(random.uniform(0, 5000), 2)},
            'MQ135': {'Benzene': round(random.uniform(0, 50), 2), 'Sulphur': round(random.uniform(0, 50), 2),
                      'Ammonia': round(random.uniform(0, 50), 2)}
        }
        
        # Emit the data to the client (React app)
        socketio.emit('sensor_data', data)
        time.sleep(1)  # Adjust sleep time to control data update frequency

# Video streaming function for Camera 1
def generate_video1():
    cap = cv.VideoCapture(0)  # Open the first camera device
    if not cap.isOpened():
        print("Error: Unable to access Camera 1")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Encode the frame to JPEG
        _, buffer = cv.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        # Send the frame to the client in the correct format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
    cap.release()

# Video streaming function for Camera 2
def generate_video2():
    cap = cv.VideoCapture(2)  # Open the second camera device
    if not cap.isOpened():
        print("Error: Unable to access Camera 2")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Encode the frame to JPEG
        _, buffer = cv.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        # Send the frame to the client in the correct format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
    cap.release()

@app.route('/video1')
def video1():
    return Response(generate_video1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video2')
def video2():
    return Response(generate_video2(), mimetype='multipart/x-mixed-replace; boundary=frame')

# SocketIO event to handle client connection
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('sensor_data', {'message': 'Welcome to the Flask server'})

# Start the sensor data generation in a separate thread
def start_data_generation():
    thread = threading.Thread(target=generate_sensor_data)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    start_data_generation()  # Start generating sensor data
    socketio.run(app, host='0.0.0.0', port=5000)
