from rest_framework import serializers
from .models import DDR, Farmer, DDRFarmer, ClusterIncharge, Variety, CropType, Source

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = "__all__"

class DDRFarmerSerializer(serializers.ModelSerializer):
    farmer = serializers.CharField(source='farmer.code')  # Expect farmer code as input

    class Meta:
        model = DDRFarmer
        fields = ['farmer', 'ddr_qty']

class DDRSerializer(serializers.ModelSerializer):
    farmers = DDRFarmerSerializer(many=True, write_only=True)
    farmers_detail = serializers.SerializerMethodField(read_only=True)
    total_qty = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DDR
        fields = [
            'cluster_incharge', 'variety', 'crop_type', 'source', 
            'delivery_date', 'farmers', 'farmers_detail', 'total_qty',
            'delivery_location', 'state'
        ]

    def get_farmers_detail(self, obj):
        ddr_farmers = DDRFarmer.objects.filter(ddr=obj)
        return DDRFarmerSerializer(ddr_farmers, many=True).data

    def get_total_qty(self, obj):
        ddr_farmers = DDRFarmer.objects.filter(ddr=obj)
        return sum(farmer.ddr_qty for farmer in ddr_farmers)

    def create(self, validated_data):
        farmers_data = validated_data.pop('farmers')
        
        # Handle cluster_incharge lookup or creation
        cluster_incharge_name = validated_data.pop('cluster_incharge')
        cluster_incharge = ClusterIncharge.objects.get(name=cluster_incharge_name)
        validated_data['cluster_incharge'] = cluster_incharge

        # Create the DDR instance
        ddr = DDR.objects.create(**validated_data)

        # Iterate through the farmers and create DDRFarmer entries
        for farmer_data in farmers_data:
            farmer_code = farmer_data.pop('farmer')
            farmer = Farmer.objects.get(code=farmer_code)
            DDRFarmer.objects.create(ddr=ddr, farmer=farmer, **farmer_data)

        return ddr


class ClusterInchargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterIncharge
        fields = "__all__"

class VarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Variety
        fields = "__all__"

class CropTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropType
        fields = "__all__"

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"
