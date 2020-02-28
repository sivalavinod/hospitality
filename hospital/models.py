from django.db import models

class Medicine(models.Model):
    dis=models.CharField(max_length=100)
    med=models.CharField(max_length=100)
    code=models.CharField(max_length=100,default=False)
