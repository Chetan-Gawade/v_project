# # Import necessary modules
# from django.db import connection
# from django.http import JsonResponse
# import json

# # Define your view function
# def get_users_by_reference_number(request):
#     # Check if the request method is GET
#     if request.method == 'GET':
#         # Define your SQL query to fetch users based on role
#         sql_query = """
#             SELECT full_name 
#             FROM user
#             WHERE role = 3
#         """

#         # Execute the SQL query using Django's database cursor
#         with connection.cursor() as cursor:
#             cursor.execute(sql_query)
#             # Fetch all rows
#             rows = cursor.fetchall()

#         # Extract full names from the fetched rows
#         full_names = [row[0] for row in rows]

#         # Return the full names as a JSON response
#         return JsonResponse({'users': full_names}, status=200)

#     # Return an error response if the request method is not GET
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)











# # import json
# # from django.http import JsonResponse
# # from django.views.decorators.http import require_POST
# # from django.db import connection

# # @require_POST
# # def get_users_by_reference_number(request):
# #     try:
# #         # Attempt to parse the JSON payload from the request body
# #         payload = json.loads(request.body.decode('utf-8'))
# #         print("Payload:", payload)

# #         # Check if 'reference_number' is present in the payload
# #         reference_number = payload.get('reference_number')
# #         if reference_number is None:
# #             return JsonResponse({'error': 'reference_number is required'}, status=400)

# #     except json.JSONDecodeError:
# #         return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

# #     except KeyError:
# #         return JsonResponse({'error': 'Missing reference_number in payload'}, status=400)

# #     # Fetch users by role using the reference_number
# #     try:
# #         with connection.cursor() as cursor:
# #             cursor.execute(
# #                 """
# #                 SELECT user_id, full_name, email
# #                 FROM user
# #                 WHERE role = 3 AND reference_number = %s
# #                 """, [reference_number]
# #             )
# #             rows = cursor.fetchall()

# #         # Extract user information from the fetched rows
# #         users = [{'user_id': row[0], 'full_name': row[1], 'email': row[2]} for row in rows]

# #         if not users:
# #             return JsonResponse({'message': 'No users found with the provided criteria'}, status=404)

# #         # Construct and return the JSON response with user information
# #         return JsonResponse({'users': users}, status=200)

# #     except Exception as e:
# #         return JsonResponse({'error': str(e)}, status=500)




# Import necessary modules
from django.db import connection
from django.http import JsonResponse
import json

def fetch_users_by_role(request):
    if request.method == 'GET':
        sql_query = """
            SELECT full_name, email, user_id
            FROM user
            WHERE role = 3
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()

        # Extract user details from the fetched rows
        users = [
            {
                "full_name": row[0],
                "email": row[1],
                "user_id": row[2]
            } for row in rows
        ]

        return JsonResponse({'users': users}, status=200)

    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
