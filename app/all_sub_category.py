from django.http import JsonResponse
from django.db import connection
import json

def get_subcategories(request):
    # Check if the request method is GET
    if request.method == 'GET':
        # Define your SQL query to fetch sub_category_id and sub_category
        sql_query = """
            SELECT sub_category_id, sub_category 
            FROM sub_category
        """

        # Execute the SQL query using Django's database cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            # Fetch all rows
            rows = cursor.fetchall()

        # Extract sub_category_id and sub_category from the fetched rows
        sub_categories = [{'sub_category_id': row[0], 'sub_category': row[1]} for row in rows]

        # Return the sub_categories as a JSON response
        return JsonResponse({'sub_categories': sub_categories}, status=200)

    # Return an error response if the request method is not GET
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
