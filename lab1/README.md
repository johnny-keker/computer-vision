# Labwork 1

## Task

Create an app that would stream a video and allow user to switch between 3 modes:

* normal
* black and white
* tresholded with configurable treshold

## Theory and App architecture

The conversion of a gray scale image into black or white, so called binary image is called binarization.
The simplest way of binarization is thresholding; setting pixels to white (or 1) if the gray value is
equal or greater than the threshold or setting to black (0) if smaller.

As a base for building app I found an app for video streaming using OpenCV and Flask libraries:

https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/

This provided me with base, but needed a lot of modifications. Basically, I just used the logic
of streaming frames into the web page. Original app used input from a webcam, I had to move to
`FileVideoStream` since I didn't want to dox myself in the example section.

Then I added the logic of tresholding and converting image to black and white. For black and white
conversion I used two steps:

1. convert to grayscale: `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`
2. apply treshold: `cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)`

In case of Tresholding mode I just use the second step with the second parameter from `GET` request.

Speaking of which...

I had to setup simple HTML forms and endpoints on backend to change the current streaming mode and
set treshold value. I know, that it looks pretty bad, but I'm not very good with frontend development.

Anyway, we have 3 buttons: `HW`, `NORMAL` and `TRESHOLD`, as well as range input for the treshold value
and we can change modes in realtime, while looped video is playing, pretty cool.

Also, I had to add `--fps` param, which is implemented using `sleep` between frames producing. Without
it frames was drawn as fast as python could generate them, which is pretty fast. Default value for
target FPS is 30.

## Usage

Requirements:

```
imutils
flask
opencv-contrib-python
```

The app takes 4 positional arguments:

* `-i` : IP address of the target device
* `-o` : Port of the target device
* `-v` : Path to the target video
* `-f` : `[optional]` target FPS, default 30

Sample usage:

```
python3 webstreaming.py -i 127.0.0.1 -o 8000 -v video.mp4
```

And then you shoud see the application on http://127.0.0.1:8000/

## Demonstration

## Conclusions

In this labwork I build app that allows user to play with video stream tresholding in realtime.

References is mentioned in the readme text as clickable liks.
