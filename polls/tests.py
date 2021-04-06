import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Pergunta
# Create your tests here.

def registra_pergunta(pergunta_text, dias):
    """
    Registra a pergunta com os campos 'pergunta_text' e a data que foi
    publicada, do qual é por padrão: presente (negativo para perguntas publicadas
    no passado, positivo para perguntas que ainda vão ser publicadas).
    """
    time = timezone.now() + datetime.timedelta(dias=dias)
    return Pergunta.objects.create(pergunta_text=pergunta_text, data_publicada=time)


class PerguntaIndexViewTests(TestCase):
    def test_sem_perguntas(self):
        """
        Se a pergunta não existe, uma mensagem apropriada será mostrada
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sem polls disponiveis.")
        self.assertQuerysetEqual(response.context['lista_perguntas'], [])

    def test_pergunta_passada(self):
        """
        Perguntas anteriores serão mostra na pagina index
        """
        registra_pergunta(pergunta_text="Pergunta Passada.", dias=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['lista_perguntas'],
            ['<Question: Pergunta Passada.>']
        )

    def test_pergunta_futura(self):
        """
        Perguntas que ainda viram não serão mostradas na pagina index
        """
        registra_pergunta(pergunta_text="Pergunta Futura.", dias=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Sem polls disponiveis.")
        self.assertQuerysetEqual(response.context['lista_perguntas'], [])

    def test_perguntas_do_passado_e_do_futuro(self):
        """
        Se perguntas do passado e também do futuro existirem, 
        serão mostrada apenas a do passado
        """
        registra_pergunta(pergunta_text="Pergunta Passada.", dias=-30)
        registra_pergunta(pergunta_text="Pergunta Futura.", dias=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['lista_perguntas'],
            ['<Question: Pergunta Passada.>']
        )

    def test_duas_perguntas_passadas(self):
        """
        A pagina index deve mostrar multiplas perguntas do passado
        """
        registra_pergunta(pergunta_text="Pergunta Passada 1.", dias=-30)
        registra_pergunta(pergunta_text="Pergunta Passada 2.", dias=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['lista_perguntas'],
            ['<Question: Pergunta Passada 2.>', '<Question: Pergunta Passada 1.>']
        )
class PerguntaModelTestes(TestCase):
    def test_foi_publicado_recentemente_com_pergunta_futura(self):
        """foi_publicado_recentemente() deve retornar False para perguntas que foram
        publicadas no futuro. """
        time = timezone.now() + datetime.timedelta(dias=30)
        pergunta_futura = Pergunta(data_publicada=time)
        self.assertIs(pergunta_futura.foi_publicado_recentemente(), False)
    
    def test_foi_publicado_recentemente_com_pergunta_antiga(self):
        """foi_publicado_recentemente() deve retornar False para perguntas que foram
        publicadas a pelo menos 1 dia atrás. """
        time = timezone.now() - datetime.timedelta(dias=1, seconds=1)
        pergunta_antiga = Pergunta(data_publicada=time)
        self.assertIs(pergunta_antiga.foi_publicado_recentemente(), False)
    
    def test_foi_publicado_recentemente_com_pergunta_recente(self):
        """foi_publicado_recentemente() deve retornar True para perguntas que foram
        publicadas hoje. """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pergunta_recente = Pergunta(data_publicada=time)
        self.assertIs(pergunta_recente.foi_publicado_recentemente(), True)

class PerguntaDetailViewTests(TestCase):
    def test_pergunta_futura(self):
        """
        A pagina detalhada de uma pergunta do futuro retorna o codigo 404

        """
        pergunta_futura = registra_pergunta(pergunta_text='Pergunta Futura.', dias=5)
        url = reverse('polls:detail', args=(pergunta_futura.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_pergunta_passada(self):
        """
        A pagina detalhada das perguntas mostra as perguntas que foram publicadas

        """
        pergunta_passada = registra_pergunta(pergunta_text='Pergunta Passada.', dias=-5)
        url = reverse('polls:detail', args=(pergunta_passada.id,))
        response = self.client.get(url)
        self.assertContains(response, pergunta_passada.pergunta_text)