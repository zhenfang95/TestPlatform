from django.contrib import admin

# Register your models here.
from MyApp.models import *

#建表后注册到admin后台
admin.site.register(DB_tucao)
admin.site.register(DB_home_href)

