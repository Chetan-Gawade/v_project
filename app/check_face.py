from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import cv2
from base64 import b64decode
import json

from .face_detection import detect_faces

@csrf_exempt
def check_faces(request):
    data = json.loads(request.body).get("image").split(",")[-1]
    content = b64decode(data)
    arr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    cheating, n_faces = detect_faces(img)
    response_result = {
        "result": cheating,
        "number_of_faces": n_faces,
    }

    return JsonResponse(
        response_result,
        status=200,
    )
