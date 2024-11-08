# Import necessary modules
from django.db import connection
from django.http import JsonResponse
import json

# Define your view function
def fetchuser(request):
    # Check if the request method is GET
    if request.method == 'GET':
        # Define your SQL query to fetch users based on role
        sql_query = """
            SELECT full_name 
            FROM user
            WHERE role = 3
        """

        # Execute the SQL query using Django's database cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            # Fetch all rows
            rows = cursor.fetchall()

        # Extract full names from the fetched rows
        full_names = [row[0] for row in rows]

        # Return the full names as a JSON response
        return JsonResponse({'users': full_names}, status=200)

    # Return an error response if the request method is not GET
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
