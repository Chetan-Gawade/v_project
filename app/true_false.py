from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
@csrf_exempt
def truefalse(request):
    if request.method == 'POST':
        # Extracting data from the POST request
        data = json.loads(request.body.decode('utf-8'))
        description = data.get('description')
        marks = data.get('marks')
        category = data.get('category')
        sub_category = data.get('sub_category')  # Corrected casing here
        question_type = data.get('type')

        option1 = data.get('option1')
        option2 = data.get('option2')
        correct_option_name = data.get('correct_option')

        options = [option1, option2]
        
        with connection.cursor() as cursor:
            try:
                # Fetching category ID
                cursor.execute("SELECT category_id FROM category WHERE category_id = %s", [category])
                category_row = cursor.fetchone()
                if category_row:
                    category_id = category_row[0]
                else:
                    return JsonResponse({'error': 'category not found'}, status=400)

                # Fetching subcategory ID 
                cursor.execute("SELECT sub_category_id FROM sub_category WHERE sub_category_id = %s", [sub_category])
                subcategory_row = cursor.fetchone()
                if subcategory_row:
                    subcategory_id = subcategory_row[0]
                else:
                    return JsonResponse({'error': 'sub_category not found'}, status=400)

                # Fetching type ID
                cursor.execute("SELECT type_id FROM question_type WHERE type = %s", [question_type])
                type_row = cursor.fetchone()
                if type_row:
                    type_id = type_row[0]  
                else:
                    return JsonResponse({'error': 'Question type not found'}, status=400)

            
                cursor.execute("""
                    INSERT INTO questions (description, sub_category_id, type_id, category_id, marks)
                    VALUES (%s, %s, %s, %s, %s)
                """, [description, subcategory_id, type_id, category_id, marks])  # Include marks here
                questions_id = cursor.lastrowid
                
                for option_text in options:
                    is_correct = 'Y' if option_text == correct_option_name else 'N'
                    cursor.execute("""
                        INSERT INTO questions_option (questions_id, `option`, is_correct)
                        VALUES (%s, %s, %s)
                    """, [questions_id, option_text, is_correct])


                return JsonResponse({'message': 'Question added successfully'}, status=201)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
