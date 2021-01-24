from flask import Flask, request, Response

import numpy as np
import json
import cv2
import base64
import sys

from scan import DocScanner
from image_parser import parse_image

app = Flask(__name__)
scanner = DocScanner()


@app.route("/api/test", methods=["POST"])
def process_img():
    r = request

    imgString = base64.b64decode(r.data)
    # print(type(r.data))

    nparr = np.frombuffer(imgString, np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    print(img_bgr.shape)
    img_cv2 = scanner.scan(img_bgr)

    response = {"message": parse_image(img_cv2)}

    # Serialize into JSON format
    response_json = json.dumps(response)

    return Response(response=response_json, status=200, mimetype="application/json")


app.run(host="0.0.0.0", port=5000)
