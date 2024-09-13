from django.urls import path
from ddr.views import get_eligible_farmers, CreateDDRView

urlpatterns = [
    path('farmers/', get_eligible_farmers, name='get_eligible_farmers'),
    path('ddr/create/', CreateDDRView.as_view(), name='create_ddr'),
]