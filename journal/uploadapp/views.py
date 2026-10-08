import os
import uuid
from django.shortcuts import render
from django.conf import settings


def upload_file(request):
    """Загрузка одного файла. Сохранение частями через chunks()."""
    context = {'errors': []}

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file is None:
            context['errors'].append('Файл не передан.')
        else:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            unique_name = f"{uuid.uuid4().hex}{ext}"

            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, unique_name)

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            context.update({
                'saved_name': unique_name,
                'original_name': uploaded_file.name,
            })
            return render(request, 'uploadapp/upload_success.html', context)

    return render(request, 'uploadapp/upload.html', context)