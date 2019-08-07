""" imagezmq: Transport OpenCV images via ZMQ.

Classes that transport OpenCV images from one computer to another. For example,
OpenCV images gathered by a Raspberry Pi camera could be sent to another
computer for displaying the images using cv2.imshow() or for further image
processing. See API and Usage Examples for details.

Copyright (c) 2017 by Jeff Bass.
License: MIT, see LICENSE for more details.
"""

import zmq
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread


class ImageSender():
    """Opens zmq REQ socket and sends images.

    Opens a zmq REQ socket on the image sending computer, often a
    Raspberry Pi, that will be sending OpenCV images and
    related text messages to the hub computer. Provides methods to
    send images or send jpg compressed images.

    Arguments:
      connect_to: the tcp address:port of the hub computer.
    """

    def __init__(self, connect_to='tcp://127.0.0.1:5555'):
        """Initializes zmq socket for sending images to the hub.

        Expects an open socket at the connect_to tcp address; it will
        connect to that remote socket after setting up the REQ
        socket on this computer.
        """

        self.zmq_context = SerializingContext()
        self.zmq_socket = self.zmq_context.socket(zmq.REQ)
        self.zmq_socket.connect(connect_to)

    def send_image(self, msg, image):
        """Sends OpenCV image and msg to hub computer.

        Arguments:
          msg: text message or image name.
          image: OpenCV image to send to hub.

        Returns:
          A text reply from hub.
        """

        if image.flags['C_CONTIGUOUS']:
            # if image is already contiguous in memory just send it
            self.zmq_socket.send_array(image, msg, copy=False)
        else:
            # else make it contiguous before sending
            image = np.ascontiguousarray(image)
            self.zmq_socket.send_array(image, msg, copy=False)
        hub_reply = self.zmq_socket.recv()  # receive the reply message
        return hub_reply

    def send_jpg(self, msg, jpg_buffer):
        """Sends msg text and jpg buffer to hub computer.

        Arguments:
          msg: image name or message text.
          jpg_buffer: bytestring containing the jpg image to send to hub.
        Returns:
          A text reply from hub.
        """

        self.zmq_socket.send_jpg(msg, jpg_buffer, copy=False)
        hub_reply = self.zmq_socket.recv()  # receive the reply message
        return hub_reply


class ImageHub():
    """Opens zmq REP socket and receives images.

    Opens a zmq REP socket on the hub compuer, for example,
    a Mac, that will be receiving and displaying or processing OpenCV images
    and related text messages. Provides methods to receive images or receive
    jpg compressed images.

    Arguments:
      open_port: (optional) the socket to open for receiving REQ requests.
    """

    def __init__(self, open_port='tcp://*:5555'):
        """Initializes zmq REP socket to receive images and text.
        """

        self.zmq_context = SerializingContext()
        self.zmq_socket = self.zmq_context.socket(zmq.REP)
        self.zmq_socket.bind(open_port)

    def recv_image(self, copy=False):
        """Receives OpenCV image and text msg.

        Arguments:
          copy: (optional) zmq copy flag.

        Returns:
          msg: text msg, often the image name.
          image: OpenCV image.
        """

        msg, image = self.zmq_socket.recv_array(copy=False)
        return msg, image

    def recv_jpg(self, copy=False):
        """Receives text msg, jpg buffer.

        Arguments:
          copy: (optional) zmq copy flag
        Returns:
          msg: text message, often image name
          jpg_buffer: bytestring jpg compressed image
        """

        msg, jpg_buffer = self.zmq_socket.recv_jpg(copy=False)
        return msg, jpg_buffer

    def send_reply(self, reply_message=b'OK'):
        """Sends the zmq REP reply message.

        Arguments:
          reply_message: reply message text, often just string 'OK'
        """
        self.zmq_socket.send(reply_message)


class SerializingSocket(zmq.Socket):
    """Numpy array serialization methods.

    Modelled on PyZMQ serialization examples.

    Used for sending / receiving OpenCV images, which are Numpy arrays.
    Also used for sending / receiving jpg compressed OpenCV images.
    """

    def send_array(self, A, msg='NoName', flags=0, copy=True, track=False):
        """Sends a numpy array with metadata and text message.

        Sends a numpy array with the metadata necessary for reconstructing
        the array (dtype,shape). Also sends a text msg, often the array or
        image name.

        Arguments:
          A: numpy array or OpenCV image.
          msg: (optional) array name, image name or text message.
          flags: (optional) zmq flags.
          copy: (optional) zmq copy flag.
          track: (optional) zmq track flag.
        """

        md = dict(
            msg=msg,
            dtype=str(A.dtype),
            shape=A.shape,
        )
        self.send_json(md, flags | zmq.SNDMORE)
        return self.send(A, flags, copy=copy, track=track)

    def send_jpg(self,
                 msg='NoName',
                 jpg_buffer=b'00',
                 flags=0,
                 copy=True,
                 track=False):
        """Send a jpg buffer with a text message.

        Sends a jpg bytestring of an OpenCV image.
        Also sends text msg, often the image name.

        Arguments:
          msg: image name or text message.
          jpg_buffer: jpg buffer of compressed image to be sent.
          flags: (optional) zmq flags.
          copy: (optional) zmq copy flag.
          track: (optional) zmq track flag.
        """

        md = dict(msg=msg, )
        self.send_json(md, flags | zmq.SNDMORE)
        return self.send(jpg_buffer, flags, copy=copy, track=track)

    def recv_array(self, flags=0, copy=True, track=False):
        """Receives a numpy array with metadata and text message.

        Receives a numpy array with the metadata necessary
        for reconstructing the array (dtype,shape).
        Returns the array and a text msg, often the array or image name.

        Arguments:
          flags: (optional) zmq flags.
          copy: (optional) zmq copy flag.
          track: (optional) zmq track flag.

        Returns:
          msg: image name or text message.
          A: numpy array or OpenCV image reconstructed with dtype and shape.
        """

        md = self.recv_json(flags=flags)
        msg = self.recv(flags=flags, copy=copy, track=track)
        A = np.frombuffer(msg, dtype=md['dtype'])
        return (md['msg'], A.reshape(md['shape']))

    def recv_jpg(self, flags=0, copy=True, track=False):
        """Receives a jpg buffer and a text msg.

        Receives a jpg bytestring of an OpenCV image.
        Also receives a text msg, often the image name.

        Arguments:
          flags: (optional) zmq flags.
          copy: (optional) zmq copy flag.
          track: (optional) zmq track flag.

        Returns:
          msg: image name or text message.
          jpg_buffer: bytestring, containing jpg image.
        """

        md = self.recv_json(flags=flags)  # metadata text
        jpg_buffer = self.recv(flags=flags, copy=copy, track=track)
        return (md['msg'], jpg_buffer)


class SerializingContext(zmq.Context):
    _socket_class = SerializingSocket

class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class VideoStream:
    def __init__(self, src=0, usePiCamera=False, resolution=(320, 240),
        framerate=32):
        # check to see if the picamera module should be used
        if usePiCamera:
            # only import the picamera packages unless we are
            # explicity told to do so -- this helps remove the
            # requirement of `picamera[array]` from desktops or
            # laptops that still want to use the `imutils` package

            # initialize the picamera stream and allow the camera
            # sensor to warmup
            self.stream = PiVideoStream(resolution=resolution,
                framerate=framerate)

        # otherwise, we are using OpenCV so initialize the webcam
        # stream

    def start(self):
        # start the threaded video stream
        return self.stream.start()

    def update(self):
        # grab the next frame from the stream
        self.stream.update()

    def read(self):
        # return the current frame
        return self.stream.read()

    def stop(self):
        # stop the thread and release any resources
        self.stream.stop()


