
"""
django后台密码：123456
建表后，需同步结构表并生效，依次执行：
python manage.py makemigrations
python manage.py migrate
"""
from django.contrib import admin

# Register your models here.
from MyApp.models import *

#建表后注册到admin后台
admin.site.register(DB_tucao)
admin.site.register(DB_home_href)
admin.site.register(DB_project)
admin.site.register(DB_apis)

