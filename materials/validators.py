from rest_framework.serializers import ValidationError
import re


def validate_youtube_link(value):
    """ Проверка, что ссылка начинается с 'https://www.youtube.com/' или 'https://youtu.be/' """
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/).+$'
    if not re.match(youtube_regex, value):
        raise ValidationError('Ссылки на сторонние ресурсы не разрешены. Используйте только ссылки на youtube.com.')
