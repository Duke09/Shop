from django.utils.translation import gettext_lazy as _
from django.urls import path

from .views import *

app_name = 'payment'

urlpatterns = [
    path(_('process/'), payment_process, name='process'),
    path(_('done/'), payment_done, name='done'),
    path(_('canceled/'), payment_canceled, name='canceled'),
]