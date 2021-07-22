from flask import Flask, render_template, Response
from camera import Camera
from plotter import Plotter
from flask import Response
import datetime


app = Flask(__name__)

counter = []
timestamps = []


@app.route('/')
def index():
    return render_template('index.html')


def gen_plot():
    while True:
        plotter = Plotter()
        output = plotter.get_plot(timestamps, counter)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + output.getvalue() + b'\r\n\r\n')


@app.route('/data_feed')
def data_feed():
    return Response(gen_plot(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_video(camera):
    while True:
        frame = camera.get_frame()
        global counter
        global timestamps
        counter.append(len(camera.get_recognized_ids()[1]))
        timestamps.append(int(datetime.datetime.now().timestamp()))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_video(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
