# from django.http import JsonResponse
# from django.db import connection
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# import json

# @method_decorator(csrf_exempt, name='dispatch')
# class FetchUserByRefNum(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             user_id = data.get('user_id')
#             reference_number = data.get('reference_number')

#             if not user_id or not reference_number:
#                 return JsonResponse({"error": "user_id and reference_number are required"}, status=400)

#         except json.JSONDecodeError as e:
#             return JsonResponse({"error": "Invalid JSON payload", "details": str(e)}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": "Invalid payload", "details": str(e)}, status=400)

#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT user_id, role
#                     FROM user
#                     WHERE user_id = %s AND reference_number = %s
#                 """, [user_id, reference_number])
#                 user = cursor.fetchone()

#                 if not user:
#                     return JsonResponse({"error": "User not found"}, status=404)
#                 if user[1] != 2:
#                     return JsonResponse({"error": "Invalid instructor details"}, status=403)

#                 cursor.execute("""
#                     SELECT user_id, full_name, email, reference_number
#                     FROM user
#                     WHERE reference_number = %s AND role = 3
#                 """, [reference_number])
#                 rows = cursor.fetchall()

#                 students = [
#                     {
#                         "user_id": row[0],
#                         "full_name": row[1],
#                         "email": row[2],
#                         "reference_number": row[3]
#                     } for row in rows
#                 ]

#             return JsonResponse(students, safe=False)
#         except Exception as e:
#             return JsonResponse({"error": "Internal server error", "details": str(e)}, status=500)


from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def fetch_user_by_ref_num(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        reference_number = data.get('reference_number')

        if not user_id or not reference_number:
            return JsonResponse({"error": "user_id and reference_number are required"}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON payload", "details": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": "Invalid payload", "details": str(e)}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT user_id, role
                FROM user
                WHERE user_id = %s AND reference_number = %s
            """, [user_id, reference_number])
            user = cursor.fetchone()

            if not user:
                return JsonResponse({"error": "User not found"}, status=404)
            if user[1] != 2:
                return JsonResponse({"error": "Invalid instructor details"}, status=403)

            cursor.execute("""
                SELECT user_id, full_name, email, reference_number
                FROM user
                WHERE reference_number = %s AND role = 3
            """, [reference_number])
            rows = cursor.fetchall()

            students = [
                {
                    "user_id": row[0],
                    "full_name": row[1],
                    "email": row[2],
                    "reference_number": row[3]
                } for row in rows
            ]

        return JsonResponse(students, safe=False)
    except Exception as e:
        return JsonResponse({"error": "Internal server error", "details": str(e)}, status=500)
