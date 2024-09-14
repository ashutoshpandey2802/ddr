from rest_framework import serializers
from .models import DDR, Farmer, DDRFarmer, ClusterIncharge, Variety, CropType, Source
from django.core.exceptions import ValidationError


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
    
    # Accept both IDs or names for cluster_incharge and variety
    cluster_incharge = serializers.CharField(write_only=True)
    variety = serializers.CharField(write_only=True)
    crop_type = serializers.CharField(write_only=True)
    source = serializers.CharField(write_only=True)

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

    def get_instance_by_name_or_id(self, model, value):
        """
        Helper method to get an instance of a model either by id or by name.
        """
        try:
            # Check if the value is a digit (i.e., ID)
            if str(value).isdigit():
                return model.objects.get(pk=value)
            # Otherwise, assume it's a name and get the instance by name
            return model.objects.get(name=value)
        except model.DoesNotExist:
            raise ValidationError(f"{model.__name__} with the given identifier '{value}' does not exist.")

    def create(self, validated_data):
        farmers_data = validated_data.pop('farmers')

        # Handle cluster_incharge
        cluster_incharge_value = validated_data.pop('cluster_incharge')
        cluster_incharge = self.get_instance_by_name_or_id(ClusterIncharge, cluster_incharge_value)

        # Handle variety
        variety_value = validated_data.pop('variety')
        variety = self.get_instance_by_name_or_id(Variety, variety_value)

        # Handle crop_type
        crop_type_value = validated_data.pop('crop_type')
        crop_type = self.get_instance_by_name_or_id(CropType, crop_type_value)

        # Handle source
        source_value = validated_data.pop('source')
        source = self.get_instance_by_name_or_id(Source, source_value)

        # Create the DDR instance
        ddr = DDR.objects.create(
            cluster_incharge=cluster_incharge,
            variety=variety,
            crop_type=crop_type,
            source=source,
            **validated_data
        )

        # Create DDRFarmer entries for each farmer
        for farmer_data in farmers_data:
            farmer_code = farmer_data.pop('farmer')
            try:
                farmer = Farmer.objects.get(code=farmer_code)
            except Farmer.DoesNotExist:
                raise serializers.ValidationError(f"Farmer with code {farmer_code} does not exist.")

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
