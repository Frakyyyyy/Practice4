from django import forms
from .models import Group, Student


class StudentFilterForm(forms.Form):
    surname_part = forms.CharField(
        label='Часть фамилии',
        required=False,
        max_length=100,
    )
    group = forms.ModelChoiceField(
        label='Группа',
        queryset=Group.objects.all(),
        required=False,
    )
    group_name_part = forms.CharField(
        label='Часть названия группы',
        required=False,
        max_length=100,
    )


class StudentAvatarForm(forms.ModelForm):
    """Форма изменения аватара с серверной валидацией."""

    MAX_SIZE = 5 * 1024 * 1024          # 5 МиБ = 5 242 880 байт
    ALLOWED_TYPES = ['image/jpeg', 'image/png']
    ALLOWED_EXTS = ['.jpg', '.jpeg', '.png']

    class Meta:
        model = Student
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if not avatar:
            raise forms.ValidationError('Выберите файл изображения.')

        if avatar.size > self.MAX_SIZE:
            raise forms.ValidationError(
                f'Размер файла не должен превышать 5 МиБ (5 242 880 байт). '
                f'Текущий размер: {avatar.size} байт.'
            )

        if avatar.content_type not in self.ALLOWED_TYPES:
            raise forms.ValidationError(
                'Разрешены только JPEG и PNG.'
            )
            
        ext = '.' + avatar.name.rsplit('.', 1)[-1].lower()
        if ext not in self.ALLOWED_EXTS:
            raise forms.ValidationError(
                'Расширение файла должно быть .jpg, .jpeg или .png.'
            )

        return avatar