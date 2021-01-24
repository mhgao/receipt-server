#### FOR TESTING PURPOSES ONLY ####

import requests
import json
import cv2
import base64

addr = "http://localhost:5000"
test_url = addr + "/api/test"

content_type = "image/jpeg"
headers = {"content-type": content_type}

with open("data/costco.png", "rb") as imgFile:
    img_encoded = base64.b64encode(imgFile.read())

response = requests.post(test_url, data=img_encoded, headers=headers)

# print(json.loads(response.text))
print(response.text)
