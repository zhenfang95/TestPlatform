from django.db import models

# Create your models here.

#通过orm的映射来操作数据库，创建表DB_tucao
class DB_tucao(models.Model):  #映射类必须继承models.Model
    user = models.CharField(max_length=30,null=True) #吐槽人名称，格式字符串，最大长度30，允许为null
    text = models.CharField(max_length=1000,null=True) #吐槽内容
    ctime = models.DateTimeField(auto_now=True) #创建时间，会自动填入时间
    #设计一个view在后台显示
    def __str__(self):
        return self.text + str(self.ctime)

#存放超链接表
class DB_home_href(models.Model):
    name = models.CharField(max_length=30,null=True) #超链接名称
    href = models.CharField(max_length=2000,null=True) #超链接内容
    def __str__(self):
        return self.name
