from django.shortcuts import render
from django.core import serializers

# Create your views here.

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from .models import Ambiente, Hospital, Respirador
from django.contrib.auth.models import AnonymousUser
class LogOut(View):
    
    def get(self, request, *args, **kwargs):
        request.session.flush()
        if hasattr(request, 'user'):
            request.user = AnonymousUser()
        return HttpResponseRedirect("/login")

class DashboardPreview(View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        respiradores_param = request.GET.getlist('respiradores')
        if len(respiradores_param):
            respiradores = Respirador.objects.filter(code__in=respiradores_param,doctor=request.user)
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
        return render(request, "preview.html", context=context)

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
        if len(ambientes):
            array_respiradores = []
            respiradores = Respirador.objects.filter(ambiente=ambientes[0]).exclude(doctor=request.user)
            for respirador in respiradores:
                array_respiradores.append({
                    "id": respirador.code,
                    "name": respirador.name,
                    "url": "https://suquir.com.ve/wp-content/uploads/2018/08/PA-700B.png"
                })
            context["respiradores_not_have"] = array_respiradores
        else:
            context["respiradores_not_have"] = []
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

        
        if "message" in request.session.keys():
            context["message"] = request.session["message"]
            del request.session["message"]
        return render(request, "home.html", context=context)

    def post(self, request, *args, **kwargs):
        respirador = request.POST.get("respirador")
        if respirador:
            respiradores = Respirador.objects.filter(code=respirador)
            if len(respiradores):
                respirador = respiradores[0]
                respirador.doctor = request.user
                respirador.save()
                request.session["message"] = {"message":"Respirador "+ respirador.code +" asignado.", "type":"success"}
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
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