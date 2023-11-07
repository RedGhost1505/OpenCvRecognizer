from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2


app = Flask(__name__)
socketio = SocketIO(app)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')


# @socketio.on('pull_in')
# def int():
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     cap = cv2.VideoCapture(0)


@socketio.on('request_frame')
def send_frame():
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # cap = cv2.VideoCapture(0)


    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Cara', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()

        emit('new_frame', {'frame': frame_data}, broadcast=True)

    # cap.release()

@socketio.on('pull_out')
def disconnection():
    cap.release()

if __name__ == '__main__':
    socketio.run(app)