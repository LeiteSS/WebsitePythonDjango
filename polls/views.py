from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from  .models import Pergunta, Resposta

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lista_perguntas'
    def get_queryset(self):
        """Retorna as ultimas cincos perguntas publicadas.
        (ignorando as que ainda virão)"""
        return Pergunta.objects.filter(data_publicada__lte=timezone.now()).order_by('-data_publicada')[:5]

class DetailView(generic.DetailView):
    model = Pergunta
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Exclui qualquer pergunta que ainda 
        não foi publicada

        """
        return Pergunta.objects.filter(data_publicada__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Pergunta
    template_name = 'polls/results.html'

def voto(request, pergunta_id):
    pergunta= get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        resposta_selecionada = pergunta.resposta_set.get(pk=request.POST['resposta'])
    except (KeyError, Resposta.DoesNotExist):
        #Atualiza o formulario de resposta
        return render(request, 'polls/detail.html', {'pergunta':pergunta, 'error_message': "Nenhuma resposta foi selecionada.",})
    else:
        resposta_selecionada.votos += 1
        resposta_selecionada.save()
        #Sempre retorna um HttpResponseRedirect depois de lidar com dados POST
        #com sucesso. Isso previne de ser respondido
        #duas vezes, caso o usuario aperte o botão preto acidentalmente
        return HttpResponseRedirect(reverse('polls:resultado', args=(pergunta.id,)))