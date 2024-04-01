from imutils.video import FileVideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

vs = None
time.sleep(2.0)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


def process_frame():
    global vs, outputFrame, lock
    while True:
        frame = vs.read()
        if frame is None:
            vs.stop()
            vs = FileVideoStream(path=args["video"]).start()
            frame = vs.read()
        frame = imutils.resize(frame, width=400)

        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
        with lock:
            outputFrame = frame.copy()
        
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-v", "--video", type=str, required=True,
        help="path to a video to play")
    args = vars(ap.parse_args())
    vs = FileVideoStream(path=args["video"]).start()
	# start a thread that will perform motion detection
    t = threading.Thread(target=process_frame)
    t.daemon = True
    t.start()
	# start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()