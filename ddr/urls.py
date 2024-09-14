from django.urls import path
from .views import root_view,get_eligible_farmers, get_cluster_incharges, get_varieties, get_crop_types, get_sources, CreateDDRView

urlpatterns = [
    path('', root_view, name='root_view'),
    path('eligible-farmers/', get_eligible_farmers, name='get_eligible_farmers'),
    path('cluster-incharges/', get_cluster_incharges, name='get_cluster_incharges'),
    path('varieties/', get_varieties, name='get_varieties'),
    path('crop-types/', get_crop_types, name='get_crop_types'),
    path('sources/', get_sources, name='get_sources'),
    path('create-ddr/', CreateDDRView.as_view(), name='create_ddr'),
]
