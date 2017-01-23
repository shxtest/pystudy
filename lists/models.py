from django.db import models

# Create your models here.


# 清单List类
class List(models.Model):
    pass


# 待办事项Item类
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)



