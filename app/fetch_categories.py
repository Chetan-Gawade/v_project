# views.py

from django.http import JsonResponse
from django.db import connection

def fetch_categories(request):
    # Define your SQL query to fetch categories
    sql_query = "SELECT category_id, category FROM category"

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        # Fetch all rows from the result set
        rows = cursor.fetchall()

    # Serialize the fetched data into JSON format
    categories = []
    for row in rows:
        category_id, category = row
        categories.append({
            'category_id': category_id,
            'category': category
        })

    # Return JSON response
    return JsonResponse({'categories': categories})
