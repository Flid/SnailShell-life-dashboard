
import time

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
    is_pi_camera = True
except ImportError:
    from cv2 import VideoCapture
    is_pi_camera = False


class RPiCamera(object):
    def __init__(self, preview=False):
        self._cap = PiCamera()
        self._cap.resolution = (640, 480)
        self._cap.framerate = 1

        if preview:
            self._cap.start_preview()

        self._raw_capture = PiRGBArray(self._cap)
        time.sleep(0.1)  # Let it stabilize

    def get_frame(self):
        self._raw_capture.truncate(0)
        self._cap.capture(self._raw_capture, format='L')
        return self._raw_capture.array

    def capture_continuous(self):
        frame_generator = self._cap.capture_continuous(
            self._raw_capture,
            format='bgr',
            use_video_port=True,
        )

        for frame in frame_generator:
            yield frame.array
            self._raw_capture.truncate(0)

    def __del__(self):
        del self._cap


class CV2Camera():
    def __init__(self):
        self._cap = VideoCapture(0)

    def get_frame(self):
        ret, img = self._cap.read()
        return img

    def capture_continuous(self):
        while True:
            yield self.get_frame()
            time.sleep(1)

    def __del__(self):
        self._cap.release()


if is_pi_camera:
    Camera = RPiCamera
else:
    Camera = CV2Camera
