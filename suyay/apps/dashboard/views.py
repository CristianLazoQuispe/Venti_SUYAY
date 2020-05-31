from django.shortcuts import render
from django.core import serializers

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Ambiente, Hospital, Respirador

class Dashboard(View):

    def get(self, request, *args, **kwargs):
        array = []
        hospitals = Hospital.objects.all()
        for hospital in hospitals:
            array.append({
                "id":hospital.id,
                "name":hospital.name
            })
        context = {
            "hospitales":array
        }

        hospital_param = request.GET.get('hospital')
        ambiente_param = request.GET.get('ambiente')

        hospitals = Hospital.objects.filter(id=hospital_param)
        ambientes = Ambiente.objects.filter(id=ambiente_param)
        print(hospitals)
        print(ambientes)
        if len(hospitals) and len(ambientes):
            respiradores = Respirador.objects.filter(ambiente=ambientes[0],doctor=request.user)
            array_respiradores = []
            for respirador in respiradores:
                array_respiradores.append({
                    "id": respirador.code,
                    "name": respirador.name,
                    "url": "https://suquir.com.ve/wp-content/uploads/2018/08/PA-700B.png"
                })
            context["respiradores"] = array_respiradores
        else:
            context["respiradores"] = []
        return render(request, "home.html", context=context)

class AmbientesAjax(View):
    
    def get(self, request, *args, **kwargs):
        hospital_param = request.GET.get('hospital')
        hospitals = Hospital.objects.filter(id=hospital_param)
        if len(hospitals):
            array = []
            ambientes = Ambiente.objects.filter(hospital=hospitals[0])
            for ambiente in ambientes:
                array.append({
                    "id":ambiente.id,
                    "name":ambiente.name
                })
            return JsonResponse({"data":array})
        else:
            return JsonResponse({})