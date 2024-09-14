from rest_framework import generics
from .models import DDR, Farmer, ClusterIncharge, Variety, CropType, Source
from .serializers import DDRSerializer, FarmerSerializer, ClusterInchargeSerializer, VarietySerializer, CropTypeSerializer, SourceSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.http import HttpResponse

# API to get eligible farmers based on Source, Crop Type, Variety, and search query for autocomplete
@api_view(['GET'])
def get_eligible_farmers(request):
    source = request.GET.get('source')
    variety = request.GET.get('variety')
    crop_type = request.GET.get('crop_type')
    search = request.GET.get('search')  # for farmer code autocomplete

    # Filter farmers based on DDR relationships
    farmers = Farmer.objects.filter(
        Q(ddr__source=source),
        Q(ddr__variety=variety),
        Q(ddr__crop_type=crop_type),
        Q(code__icontains=search) if search else Q()
    ).distinct()  # Use distinct to avoid duplicates
    
    serializer = FarmerSerializer(farmers, many=True)
    return Response(serializer.data)

# API to create DDR
class CreateDDRView(generics.CreateAPIView):
    serializer_class = DDRSerializer

# APIs to fetch the dropdown data
@api_view(['GET'])
def get_cluster_incharges(request):
    cluster_incharges = ClusterIncharge.objects.all()
    serializer = ClusterInchargeSerializer(cluster_incharges, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_varieties(request):
    varieties = Variety.objects.all()
    serializer = VarietySerializer(varieties, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_crop_types(request):
    crop_types = CropType.objects.all()
    serializer = CropTypeSerializer(crop_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_sources(request):
    sources = Source.objects.all()
    serializer = SourceSerializer(sources, many=True)
    return Response(serializer.data)


from django.http import HttpResponse

def root_view(request):
    return HttpResponse("Welcome to the Django application!")

class UpdateDDRView(generics.UpdateAPIView):
    queryset = DDR.objects.all()
    serializer_class = DDRSerializer
    
class DeleteDDRView(generics.DestroyAPIView):
    queryset = DDR.objects.all()
    serializer_class = DDRSerializer
