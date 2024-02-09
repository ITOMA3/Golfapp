from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=100)
    average_score = models.IntegerField(default=0)  # FloatFieldからIntegerFieldに変更
    gender = models.CharField(max_length=1, choices=(('M', '男'), ('F', '女')))
    is_etiquette_leader = models.BooleanField(default=False)