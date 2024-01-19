import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
from flask import Flask, render_template, request, make_response, Response

import cv2
import numpy as np
from binascii import a2b_base64
import base64
import mediapipe as mp

import time

image = None

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

app = Flask(__name__)

# with mp_hands.Hands(
#     model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5
#     ) as hands:
#         # To improve performance, optionally mark the image as not writeable to
#         # pass by reference.
#         image.flags.writeable = False
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = hands.process(image)

#         # Draw the hand annotations on the image.
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         # Initially set finger count to 0 for each cap
#         fingerCount = 0

#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # Get hand index to check label (left or right)
#                 handIndex = results.multi_hand_landmarks.index(hand_landmarks)
#                 handLabel = results.multi_handedness[handIndex].classification[0].label

#                 # Set variable to keep landmarks positions (x and y)
#                 handLandmarks = []

#                 # Fill list with x and y positions of each landmark
#                 for landmarks in hand_landmarks.landmark:
#                     handLandmarks.append([landmarks.x, landmarks.y])


#                 # Draw hand landmarks
#                 mp_drawing.draw_landmarks(
#                     image,
#                     hand_landmarks,
#                     mp_hands.HAND_CONNECTIONS,
#                     mp_drawing_styles.get_default_hand_landmarks_style(),
#                     mp_drawing_styles.get_default_hand_connections_style(),
#                 )


def gen_img():
    global image
    while True:
        if not (image is None):

            try:
                with mp_hands.Hands(
                    model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5,
                ) as hands:
                    # To improve performance, optionally mark the image as not writeable to
                    # pass by reference.
                    image.flags.writeable = False
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image)

                    # Draw the hand annotations on the image.
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    # Initially set finger count to 0 for each cap
                    fingerCount = 0

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Get hand index to check label (left or right)
                            handIndex = results.multi_hand_landmarks.index(
                                hand_landmarks
                            )
                            handLabel = (
                                results.multi_handedness[handIndex]
                                .classification[0]
                                .label
                            )

                            # Set variable to keep landmarks positions (x and y)
                            handLandmarks = []

                            # Fill list with x and y positions of each landmark
                            for landmarks in hand_landmarks.landmark:
                                handLandmarks.append([landmarks.x, landmarks.y])

                            # Draw hand landmarks
                            mp_drawing.draw_landmarks(
                                image,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                mp_drawing_styles.get_default_hand_connections_style(),
                            )

                ret, buffer = cv2.imencode(".jpg", cv2.flip(image, 1))
                image = buffer.tobytes()

                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + image + b"\r\n"
                )
            except Exception as e:
                pass


@app.route("/")
def index():
    return render_template("index.html", width=320, height=240)


@app.route("/img_data", methods=["POST"])
def readr():
    global image

    data = request.get_json()
    data = data.replace("data:image/png;base64,", "")

    nparr = np.frombuffer(base64.b64decode(data), np.uint8)

    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display image
    # cv2.imshow("MediaPipe Hands", image)

    return data


@app.route("/video_feed", methods=["GET"])
def video_feed():
    return Response(gen_img(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, ssl_context="adhoc")
