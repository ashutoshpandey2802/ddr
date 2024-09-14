
from django.contrib import admin
from django.urls import path,include
from ddr.views import CreateDDRView, get_eligible_farmers, get_cluster_incharges, get_varieties, get_crop_types, get_sources
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-ddr/', CreateDDRView.as_view(), name='create-ddr'),
    path('eligible-farmers/', get_eligible_farmers, name='eligible-farmers'),
    path('cluster-incharges/', get_cluster_incharges, name='cluster-incharges'),
    path('varieties/', get_varieties, name='varieties'),
    path('crop-types/', get_crop_types, name='crop-types'),
    path('sources/', get_sources, name='sources'),
]
urlpatterns += staticfiles_urlpatterns()