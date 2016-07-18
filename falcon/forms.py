from django.forms import CharField, ModelForm, PasswordInput, HiddenInput, ValidationError, DateTimeField
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from models import FlightPlan, Device, Mission
from django.forms import extras

import uuid
import datetime

class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['email'].required = True

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CreateFlightPlanForm(ModelForm):
    class Meta:
        model = FlightPlan
        fields = ['name', 'data']

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CreateFlightPlanForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['data'].widget = HiddenInput()

    def save(self, request, commit=True):
        # Save the flghtplan ... make sure we store the name as ascii.
        fp = super(CreateFlightPlanForm, self).save(commit=False)
        fp.created_at = datetime.datetime.now()
        fp.modified_at = datetime.datetime.now()
        fp.creator = request.user
        fp.uid = uuid.uuid1().hex
        fp.data = self.cleaned_data['data'].encode('ascii')
        fp.name = self.cleaned_data['name'].encode('ascii')
        if commit:
            fp.save()
        return fp


class RegisterDeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'uid']

    def save(self, request, commit=True):
        # Save the device
        device = Device.objects.get(uid=self.cleaned_data['uid'])
        device.name = self.cleaned_data['name']
        device.modified_at = datetime.datetime.now()
        device.registered = True
        device.creator = request.user
        if commit:
            device.save()
        return device

    def clean_uid(self):
        uid = self.cleaned_data['uid']
        try:
            device = Device.objects.get(uid=uid)
            if device.registered == True:
                raise ValidationError("Device already registered.")
        except ObjectDoesNotExist:
            raise ValidationError("Device not found, please check the UID.")

        return device.uid


class CreateMissionForm(ModelForm):
    start_time = DateTimeField(widget=extras.SelectDateWidget)
    class Meta:
        model = Mission
        fields = ['name', 'flight_plan', 'device', 'start_time']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', 'None')
        super(CreateMissionForm, self).__init__(*args, **kwargs)
        self.fields['device'].queryset = Device.objects.filter(creator=self.user)
        self.fields['flight_plan'].queryset = FlightPlan.objects.filter(creator=self.user)

    def save(self, request, commit=True):
        # Save the flghtplan ... make sure we store the name as ascii.
        mission = super(CreateMissionForm, self).save(commit=False)
        mission.created_at = datetime.datetime.now()
        mission.modified_at = datetime.datetime.now()
        mission.creator = request.user
        mission.uid = uuid.uuid1().hex
        mission.flight_plan = self.cleaned_data['flight_plan']
        mission.device = self.cleaned_data['device']
        mission.start_time = self.cleaned_data['start_time']
        mission.name = self.cleaned_data['name'].encode('ascii')
        if commit:
            mission.save()
        return mission

class LiveMissionForm(ModelForm):
    flight_plan = CharField(max_length=200)
    name = CharField(max_length=200)
    device = CharField(max_length=200)
    start_time = CharField(max_length=200)

    class Meta:
        model = Mission
        fields = ['flight_plan', 'start_time', 'name', 'device']
