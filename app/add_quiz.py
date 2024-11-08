from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def fetch_all(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')

        # Fetching all categories from the category table
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT category_id, category
                FROM category
            """)
            categories = cursor.fetchall()

        # Fetching subcategories based on the selected category
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT sub_category_id, sub_category
                FROM sub_category
                WHERE category_id = %s
            """, [category_id])
            subcategories = cursor.fetchall()

        # Fetching all types from the question_type table
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT type
                FROM question_type
            """)
            types = cursor.fetchall()

        # Extracting category, subcategory, and type names from the fetched data
        category_data = [{'id': cat[0], 'name': cat[1]} for cat in categories]
        subcategory_data = [{'id': sub[0], 'name': sub[1]} for sub in subcategories]
        type_names = [type[0] for type in types]

        # Constructing the response dictionary
        response_data = {
            'categories': category_data,
            'subcategories': subcategory_data,
            'types': type_names
        }

        return JsonResponse(response_data, safe=False)









