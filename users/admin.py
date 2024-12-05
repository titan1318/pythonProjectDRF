from django.contrib import admin
<<<<<<< HEAD
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'city', 'phone')
    list_filter = ('email', 'phone',)
    search_fields = ('email', 'phone', 'city',)
=======

# Register your models here.
>>>>>>> 189608c909cf437c2d8bfea0aafa445bf4172ede
