from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Pergunta(models.Model):
    pergunta_text = models.CharField(max_length=200)
    data_publicada = models.DateTimeField('Data Publicada')

    def __str__(self):
        return self.pergunta_text
    
    def foi_publicado_recentemente(self):
        agora = timezone.now()
        return agora - datetime.timedelta(days=1) <= self.data_publicada <= agora

    foi_publicado_recentemente.admin_order_field = 'data_publicada'
    foi_publicado_recentemente.boolean = True
    foi_publicado_recentemente.short_description = 'Publicado recentemente?'
class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta_text = models.CharField(max_length=200)
    estrela = models.IntegerField(default=0)

    def __str__(self):
        return self.resposta_text
    

