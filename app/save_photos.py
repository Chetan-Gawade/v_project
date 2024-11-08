# import base64
# import json
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def save_photos(request):
#     if request.method == 'POST':
#         try:
#             json_data = json.loads(request.body)
#             user_id = json_data.get('user_id')
#             exam_id = json_data.get('exam_id')
#             photo1_base64 = json_data.get('photo1_base64')
#             photo2_base64 = json_data.get('photo2_base64')
#             photo3_base64 = json_data.get('photo3_base64')
#             print(photo1_base64)
#             print(photo2_base64)
#             print(photo3_base64)
 
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT photo FROM user WHERE user_id = %s", [user_id])
#                 user_photo = cursor.fetchone()
#                 print(user_photo)
                
#                 # if user_role and user_role[0] == 3:
#                     # Handle image data
#                 # photo1_base64 = request.POST.get('photo1_base64')
#                 # photo2_base64 = request.POST.get('photo2_base64')
#                 # photo3_base64 = request.POST.get('photo3_base64')

#                 # Check if any photo data is missing
#                 if None in (photo1_base64, photo2_base64, photo3_base64):
#                     return JsonResponse({'status': 'error', 'message': 'Photo data missing'})

#                 # Decode Base64 strings to bytes
#                 # photo1_bytes = base64.b64decode(photo1_base64)
#                 # photo2_bytes = base64.b64decode(photo2_base64)
#                 # photo3_bytes = base64.b64decode(photo3_base64)

#                 # Save photos to the database or storage
#                 # cursor.execute("INSERT INTO authenticationphoto (exam_id, user_id, `Photo 1`, `Photo 2`, `Photo 3`) VALUES (%s, %s, %s, %s)",
#                 #                 [exam_id, user_id, photo1_bytes, photo2_bytes, photo3_bytes])

#                 return JsonResponse({'status': 'success', 'message': 'Photos saved successfully'})
#                 # else:
#                 #     return JsonResponse({'status': 'error', 'message': 'User does not have the required role'})
 
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
 
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
import base64
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import cv2
from .verification import *


def decode_image(mime_data: str):
    base64_data = mime_data.split(",")[1]
    im_bytes = base64.b64decode(base64_data)
    img = cv2.imdecode(np.frombuffer(im_bytes, dtype=np.int8), cv2.IMREAD_COLOR)
    return img


@csrf_exempt
def save_photos(request):
    if request.method == 'POST':
        try:
            # Assuming the data contains 'user_id'
            user_id = request.POST.get('user_id')
            thereshold = 0.6

            # Check if the user has role=3 before saving
            with connection.cursor() as cursor:
                cursor.execute("SELECT role FROM user WHERE user_id = %s", [user_id])
                user_role = cursor.fetchone()

                if user_role and user_role[0] == 3:
                    # Handle image data
                    photo1_base64 = request.POST.get('photo1_base64')
                    photo2_base64 = request.POST.get('photo2_base64')
                    photo3_base64 = request.POST.get('photo3_base64')

                    # Check if any photo data is missing
                    if None in (photo1_base64, photo2_base64, photo3_base64):
                        return JsonResponse(
                            {"status": "error", "message": "Photo data missing"},
                            status=400,
                        )

                    photo1_img = decode_image(photo1_base64)
                    photo2_img = decode_image(photo2_base64)
                    photo3_img = decode_image(photo2_base64)

                    photos = [photo1_img, photo2_img, photo3_img]

                    # Retrieve profile photo
                    cursor.execute(
                        "SELECT photo FROM user WHERE user_id = %s", [user_id]
                    )
                    profile_photo = cursor.fetchone()[0]

                    profile_img = decode_image(profile_photo)

                    model = load_model("./app/vgg-face2_weights.pt")
                    detector = load_fd_model()

                    try:
                        results = predict(model, profile_img, photos, detector)
                    except ValueError as e:
                        return JsonResponse(
                            {"verified": False, "error": str(e)}, status=401
                        )
                    except RuntimeError as e:
                        return JsonResponse(
                            {"verified": False, "error": str(e)}, status=500
                        )

                    verified = all(map(lambda x: x >= thereshold, results))

                    return JsonResponse(
                        {"verified": verified, "results": results}, status=200
                    )
                else:
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "User does not have the required role",
                        },
                        status=401,
                    )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )







