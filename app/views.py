# # from django.shortcuts import render
# # Uncomment once django rest framework is installed
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import ImageUploadSerializer

# from .face_detection import detect_faces
# import os
# import numpy as np
# import cv2


# # Aaryadev Ghosalkar
# # Had to change API a little bit this now works for File uploads and Blob (React Frontend needs to send Blobs)
# # def detect_faces(image):
# #     # Load the pre-trained face detection model

# #     face_cascade = cv2.CascadeClassifier(
# #         cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# #     )

# #     # Read the image
# #     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# #     # Detect faces
# #     faces = face_cascade.detectMultiScale(
# #         gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
# #     )

# #     return len(faces) > 1, len(faces)


# class FaceDetectionView(APIView):
#     def post(self, request, *args, **kwargs):
#         """
#         This Function handles a post request made to the API (http://localhost:8000/api/detect_faces/).
#         This function is responsible for decoding the image as well as running the OpenCV2 face detection model
#         it returns a boolean (cheating) which is true if there is more than 1 face detected

#         Args:
#             request: Request is automatically passed by django

#         Returns:
#             A Response containing {result: boolean, number_of_faces: integer}
#         """
#         serializer = ImageUploadSerializer(
#             data=request.data
#         )  # Checks if this is a file upload...
#         if serializer.is_valid():
#             image = serializer.validated_data["image"]
#             image_path = f"temp_{image.name}"

#             with open(image_path, "wb+") as temp_file:
#                 for chunk in image.chunks():
#                     temp_file.write(chunk)
#             image = cv2.imread(image_path)

#             result, n_faces = detect_faces(image)
#             os.remove(image_path)

#             return Response(
#                 {"result": result, "number_of_faces": n_faces},
#                 status=status.HTTP_200_OK,
#             )
#         else:  # Assumes this is a Blob i.e coming from a webcam feed not a saved image
#             content = request.data["image"].read()  # Some kind of django InMemoryImage
#             arr = np.frombuffer(content, np.uint8)
#             img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

#             cheating, n_faces = detect_faces(img)

#             response_result = {"result": cheating, "number_of_faces": n_faces}

#             # print(response_result)

#             return Response(
#                 response_result,
#                 status=status.HTTP_200_OK,
#             )
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# from .face_detection import detect_faces
# from base64 import b64decode
# import numpy as np
# import cv2

# from .verification import *


# def decode_image(mime_data: str):
#     base64_data = mime_data.split(",")[1]
#     im_bytes = b64decode(base64_data)
#     img = cv2.imdecode(np.frombuffer(im_bytes, dtype=np.int8), cv2.IMREAD_COLOR)
#     return img


# @csrf_exempt
# def detect_face_endpoint(request):
#     if request.method == "POST":
#         profile_data = request.POST.get("profile")
#         thereshold = 0.8
#         current = request.POST.get("image")
#         if not profile_data:
#             return JsonResponse(
#                 {
#                     "status": "error",
#                     "message": "profile image was not provided",
#                 },
#                 status=400,
#             )
#         elif not current:
#             return JsonResponse(
#                 {
#                     "status": "error",
#                     "message": "Webcam image was not provided",
#                 },
#                 status=400,
#             )

#         try:
#             profile_img = decode_image(profile_data)
#             current_img = decode_image(current)
#         except Exception as e:
#             return JsonResponse(
#                 {
#                     "status": "error",
#                     "message": f"Error in decoding images error: {e}",
#                 },
#                 status=400,
#             )

#         img_valid, num_faces = detect_faces(current_img)

#         if not img_valid:
#             return JsonResponse(
#                 {
#                     "verfied": img_valid,
#                     "number_of_faces": num_faces,
#                     "reason": "Multiple faces detected",
#                 },
#                 status=200,
#             )

#         model = load_model("./face_detection/vgg-face2_weights.pt")
#         detector = load_fd_model()

#         try:
#             results = predict(model, profile_img, [current_img], detector)
#         except ValueError as e:
#             return JsonResponse({"verified": False, "error": str(e)}, status=401)
#         except RuntimeError as e:
#             return JsonResponse({"verified": False, "error": str(e)}, status=500)

#         return JsonResponse(
#             {
#                 "verfied": img_valid and (results[0] >= thereshold),
#                 "number_of_faces": num_faces,
#                 "similarity": results,
#             },
#             status=200,
#         )
#     else:
#         return JsonResponse(
#             {"status": "error", "message": f"Invalid request method {request.method}"},
#             status=405,
#         )


from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .face_detection import detect_faces
from base64 import b64decode
import numpy as np
import cv2

from .verification import *


def decode_image(mime_data: str):
    base64_data = mime_data.split(",")[1]
    im_bytes = b64decode(base64_data)
    img = cv2.imdecode(np.frombuffer(im_bytes, dtype=np.int8), cv2.IMREAD_COLOR)
    return img


@csrf_exempt
def detect_face_endpoint(request):
    if request.method == "POST":
        profile_data = request.POST.get("profile")
        thereshold = 0.6
        current = request.FILES.get("image")

        if not profile_data:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "profile image was not provided",
                },
                status=400,
            )
        elif not current:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Webcam image was not provided",
                },
                status=400,
            )

        try:
            profile_img = decode_image(profile_data)
            current_img = cv2.imdecode(
                np.frombuffer(current.read(), np.uint8), cv2.IMREAD_COLOR
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Error in decoding images error: {e}",
                },
                status=400,
            )

        img_valid, num_faces = detect_faces(current_img)

        if not img_valid:
            return JsonResponse(
                {
                    "verfied": img_valid,
                    "number_of_faces": num_faces,
                    "reason": "Multiple faces detected or no face detected",
                },
                status=200,
            )

        model = load_model("./app/vgg-face2_weights.pt")
        detector = load_fd_model()

        try:
            results = predict(model, profile_img, [current_img], detector)
        except ValueError as e:
            return JsonResponse({"verified": False, "error": str(e)}, status=401)
        except RuntimeError as e:
            return JsonResponse({"verified": False, "error": str(e)}, status=500)

        return JsonResponse(
            {
                "verfied": img_valid and (results[0] >= thereshold),
                "number_of_faces": num_faces,
                "similarity": results,
            },
            status=200,
        )
    else:
        return JsonResponse(
            {"status": "error", "message": f"Invalid request method {request.method}"},
            status=405,
        )
    