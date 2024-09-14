
from django.contrib import admin
from django.urls import path,include
from ddr.views import CreateDDRView, get_eligible_farmers, get_cluster_incharges, get_varieties, get_crop_types, get_sources
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ddr.urls')),  
]
urlpatterns += staticfiles_urlpatterns()