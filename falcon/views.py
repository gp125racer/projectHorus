import django

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from forms import UserForm, CreateFlightPlanForm, RegisterDeviceForm, CreateMissionForm, LiveMissionForm
from django.views.generic import View, ListView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from models import FlightPlan, Device, Mission

import datetime
import uuid

def index(request):
    context = {}
    if request.user.is_authenticated():
        return render(request, 'falcon/control_panel.html', context)
    else:
        return render(request, 'falcon/index.html', context)

class RegisterView(View):
    def post(self, request):
        uf = UserForm(request.POST, prefix='user')
        if uf.is_valid():
            uf.save()
        else:
            #raise form errors
            return django.shortcuts.render_to_response('falcon/register.html', dict(form=uf), context_instance=django.template.RequestContext(request))
        return django.http.HttpResponseRedirect("/")

    def get(self, request):
        uf = UserForm(prefix='user')
        return django.shortcuts.render_to_response('falcon/register.html', dict(form=uf), context_instance=django.template.RequestContext(request))


class CreateFlightPlanView(LoginRequiredMixin, View):
    login_url = '/login'
    def post(self, request):
        fp = CreateFlightPlanForm(request.POST)
        if fp.is_valid():
            fp.save(request)
        else:
            #raise form errors
            return django.shortcuts.render_to_response('falcon/flightplan/create.html', dict(form=fp), context_instance=django.template.RequestContext(request))
        return django.http.HttpResponseRedirect("/flightplan/list")

    def get(self, request):
        fp = CreateFlightPlanForm()
        return django.shortcuts.render_to_response('falcon/flightplan/create.html', dict(form=fp), context_instance=django.template.RequestContext(request))


class ListFlightPlanView(LoginRequiredMixin, ListView):
    template_name = 'falcon/flightplan/list.html'

    def get_queryset(self):
        return FlightPlan.objects.filter(creator=self.request.user)


class DeleteFlightplanView(LoginRequiredMixin, DeleteView):
    model = FlightPlan
    success_url = reverse_lazy('flightplan_list')


class RegisterDeviceView(LoginRequiredMixin, View):
    login_url = '/login'
    def post(self, request):
        rf = RegisterDeviceForm(request.POST)
        if rf.is_valid():
            rf.save(request)
        else:
            #raise form errors
            return django.shortcuts.render_to_response('falcon/device/create.html', dict(form=rf), context_instance=django.template.RequestContext(request))
        return django.http.HttpResponseRedirect("/device/list")

    def get(self, request):
        rf = RegisterDeviceForm()
        return django.shortcuts.render_to_response('falcon/device/create.html', dict(form=rf), context_instance=django.template.RequestContext(request))


class ListDeviceView(LoginRequiredMixin, ListView):
    template_name = 'falcon/device/list.html'

    def get_queryset(self):
        return Device.objects.filter(creator=self.request.user)


class DeleteDeviceView(LoginRequiredMixin, DeleteView):
    model = Device
    success_url = reverse_lazy('device_list')


class UpdateDeviceView(LoginRequiredMixin, UpdateView):
    model = Device
    template_name = "falcon/device/update.html"
    success_url = reverse_lazy('device_list')
    fields = ['name', 'registered']


class CreateMissionView(LoginRequiredMixin, View):
    login_url = '/login'
    def post(self, request):
        mf = CreateMissionForm(request.POST, user=request.user)
        if mf.is_valid():
            mf.save(request)
        else:
            #raise form errors
            return django.shortcuts.render_to_response('falcon/mission/create.html', dict(form=mf), context_instance=django.template.RequestContext(request))
        return django.http.HttpResponseRedirect('/mission/list')

    def get(self, request):
        mf = CreateMissionForm(user=request.user)
        return django.shortcuts.render_to_response('falcon/mission/create.html', dict(form=mf), context_instance=django.template.RequestContext(request))


class ListMissionView(LoginRequiredMixin, ListView):
    template_name = 'falcon/mission/list.html'

    def get_queryset(self):
        return Mission.objects.filter(creator=self.request.user)


class DeleteMissionView(LoginRequiredMixin, DeleteView):
    model = Mission
    success_url = reverse_lazy('mission_list')


class UpdateMissionView(LoginRequiredMixin, UpdateView):
    model = Mission
    template_name = "falcon/mission/update.html"
    success_url = reverse_lazy('mission_list')
    fields = ['name', 'flight_plan', 'start_time', 'device']


class FetchMissionView(ListView):
    def get_queryset(self, device_uid):
        eligible_missions = Mission.objects.filter(device__uid=device_uid, start_time__lte=datetime.datetime.now()).exclude(active=True).exclude(completed=True).order_by('start_time')
        for mission in eligible_missions:
            #just return the one that is farthest away from it's start time.
            return mission.as_dict()
        return {}

    def get(self, request, *args, **kwargs):
        fetched_work = self.get_queryset(kwargs.get('device_uid', None))
        return JsonResponse(fetched_work)

class AcceptMissionView(UpdateView):
    def get(self, request, *args, **kwargs):
        mission_uid = uuid.UUID(kwargs.get('muid', None))
        device_uid = uuid.UUID(kwargs.get('duid', None))
        try:
            device = Device.objects.get(uid=device_uid.hex)
            mission = Mission.objects.get(uid=mission_uid.hex)
            mission.active = True
            mission.modified_at = datetime.datetime.now()
            mission.save()
            success = 1
        except ObjectDoesNotExist:
            success = 0
        except Exception, e:
            success = 0
        return JsonResponse({"success":success})

class StopMissionView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        mission_id = int(kwargs.get('mission_id', None))
        try:
            mission = Mission.objects.get(id=mission_id)
            mission.active = False
            mission.modified_at = datetime.datetime.now()
            mission.save()
            #broadcast message to device to cancel operations here
            success = 1
        except ObjectDoesNotExist:
            success = 0
        except Exception, e:
            success = 0
        return redirect('mission_list')

class StartMissionView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        mission_id = int(kwargs.get('mission_id', None))
        try:
            mission = Mission.objects.get(id=mission_id)
            mission.active = False
            mission.start_time = datetime.datetime.now()
            mission.modified_at = datetime.datetime.now()
            mission.save()
            success = 1
        except ObjectDoesNotExist:
            success = 0
        except Exception, e:
            success = 0
        return redirect('mission_list')

class CompletedMissionView(UpdateView):
    def get(self, request, *args, **kwargs):
        mission_uid = kwargs.get('mission_uid', None)
        try:
            mission = Mission.objects.get(uid=mission_uid)
            mission.active = False
            mission.completed = True
            mission.modified_at = datetime.datetime.now()
            mission.save()
            success = 1
        except ObjectDoesNotExist:
            success = 0
        except Exception, e:
            success = 0
        return JsonResponse({"success":success})

class LiveMissionView(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, *args, **kwargs):
        mission_uid = kwargs.get('mission_uid', None)
        mission = Mission.objects.get(uid=mission_uid)
        data = mission.as_dict()
        data.update({'flight_plan':data.get('flight_plan').get('name')})
        mf = LiveMissionForm(initial=data)
        return django.shortcuts.render_to_response('falcon/mission/live.html', dict(form=mf), context_instance=django.template.RequestContext(request))

