import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import RegisteredModel, Robot


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            # Загружаем JSON-данные из запроса
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Не корректный формат данных. Необходимо загрузить данные в формате JSON'},
                                status=400)

        # Получаем данные из JSON
        model = data.get('model')
        version = data.get('version')
        created_str = data.get('created')

        # Проверка обязательных полей
        if not all([model, version, created_str]):
            return JsonResponse({'error': 'Отсутствуют обязательные поля: модель, версия, создано'}, status=400)

        # Парсим дату из строки
        created = parse_datetime(created_str)
        if not created:
            return JsonResponse({'error': 'Неверный формат даты. Должен быть указанынй формат - YYYY-MM-DD HH:MM:SS'}, status=400)

        # Проверка существования модели и версии в RegisteredModel
        try:
            registered_model = RegisteredModel.objects.get(model_name=model, version=version)
        except RegisteredModel.DoesNotExist:
            return JsonResponse({
                'error': f"Модель '{model}' с версией '{version}' не зарегистрирована."
            }, status=400)

        # Создаём запись в базе данных
        robot = Robot.objects.create(registered_model=registered_model, created=created)

        # Возвращаем успешный ответ с данными
        return JsonResponse({
            'message': 'Робот успешно создан',
            'robot': {
                'serial': str(robot.serial),
                'model': robot.registered_model.model_name,
                'version': robot.registered_model.version,
                'created': robot.created.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=201)

    return JsonResponse({'error': 'Разрешен только метод POST.'}, status=405)
