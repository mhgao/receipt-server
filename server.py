from flask import Flask, request, Response

import numpy as np
import json
import cv2
import base64

from parser import parse_image

app = Flask(__name__)

@app.route('/api/test', methods=['POST'])
def process_img():
    r = request

    imgString = base64.b64decode(r.data)

    nparr = np.frombuffer(imgString, np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

    response = {"message": parse_image(img)}

    # Serialize into JSON format
    response_json = json.dumps(response)

    return Response(response=response_json, status=200, mimetype="application/json")

app.run(host="0.0.0.0", port=5000)
