import cv2
from flask import Flask, render_template, Response

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

app = Flask(__name__)

def gen():
    
    while True:
        rect, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imwrite('caras.jpg', img)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('caras.jpg', 'rb').read() + b'\r\n')
        
    cap.release()

@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')
    

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run() 