from gc import get_objects
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cidade, Imovei, Visita

# @login_required(login_url='/auth/logar')
def home(request):

    preco_minimo = request.POST.get('preco_minimo')
    preco_maximo = request.POST.get('preco_maximo')
    cidade = request.POST.get('cidade')
    tipo = request.POST.getlist('tipo')
    cidades = Cidade.objects.all()

    if preco_maximo or preco_minimo or cidade or tipo :
        if not preco_minimo :
            preco_minimo = 0
        if not preco_maximo :
            preco_maximo = 999999999
        if not tipo:
            tipo = ['A', 'C']

        imoveis = Imovei.objects.filter(valor__gte=preco_minimo).filter(valor__lte=preco_maximo).filter(tipo_imovel__in=tipo)
    else:
        imoveis = Imovei.objects.all()

    return render(request, 'home.html', {'imoveis' : imoveis, 'cidades' : cidades})


@login_required(login_url='/auth/logar')
def imovel(request, id):
    imovel = get_object_or_404(Imovei, id=id)
    sugestoes = Imovei.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]
    return render(request, 'imovel.html', {'imovel' : imovel, 'sugestoes' : sugestoes, 'id' : id})

@login_required(login_url='/auth/logar')
def agendar_visitas(request):
    usuario = request.user
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.get('id_imovel')

    visitas = Visita(
        imovel_id=id_imovel,
        usuario=usuario,
        dia=dia,
        horario=horario
    )
    visitas.save()

    return redirect('/agendamentos')

@login_required(login_url='/auth/logar')
def agendamentos(request):
    visitas = Visita.objects.filter(usuario=request.user)
    return render(request, 'agendamentos.html', {'visitas' : visitas})

@login_required(login_url='/auth/logar')
def cancelar_agendamento(request, id):
    visita = get_object_or_404(Visita, id=id)
    visita.status = 'C'
    visita.save()
    return redirect('/agendamentos')