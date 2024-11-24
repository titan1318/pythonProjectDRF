from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson



class Command(BaseCommand):
    help = 'Создаёт группу "Модераторы" и назначает права на редактирование курсов и уроков'

    def handle(self, *args, **kwargs):

        moderators_group, created = Group.objects.get_or_create(name="Модераторы")

        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        change_course_permission = Permission.objects.get(
            codename="change_course", content_type=course_content_type
        )
        change_lesson_permission = Permission.objects.get(
            codename="change_lesson", content_type=lesson_content_type
        )

        moderators_group.permissions.add(change_course_permission, change_lesson_permission)

        self.stdout.write(self.style.SUCCESS('Группа "Модераторы" успешно создана и права назначены.'))
