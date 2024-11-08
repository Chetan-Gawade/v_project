from django.http import JsonResponse
from django.db import connection, transaction
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_subcategory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subcategory_name = data.get('subcategory_name')
            category_data = data.get('category')

            if category_data is None:
                raise ValueError('category data is missing')

            category_id = category_data.get('category_id')
            category_name = category_data.get('category_name')

            if category_id is None and category_name is None:
                raise ValueError('Category ID or Category Name is required')

            if category_id:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT category_id, category FROM Category WHERE category_id = %s", [category_id])
                    category_exists = cursor.fetchone()

                if not category_exists:
                    raise ValueError('Selected category does not exist')

            elif category_name:
                # Insert new category and get the generated ID
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO Category (category) VALUES (%s)", [category_name])
                    transaction.commit()
                    category_id = cursor.lastrowid

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        except ValueError as ve:
            return JsonResponse({'success': False, 'error': str(ve)}, status=400)

        if subcategory_name and category_id:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO sub_category(sub_category, category_id) VALUES (%s, %s)", [subcategory_name, category_id])
                    transaction.commit()

                return JsonResponse({'success': True, 'message': 'sub_category added successfully'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            missing_fields = []
            if not subcategory_name:
                missing_fields.append('subcategory_name')
            if not category_id:
                missing_fields.append('category_id')

            return JsonResponse({'success': False, 'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
