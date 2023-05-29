from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import TourPackage, Hotel, TouristPlace, State, District, TouristPlaceImage

class TourPackageSerializer(serializers.ModelSerializer):
    hotel_name = serializers.SerializerMethodField()

    def get_hotel_name(self, instance):
        return [hotel.name for hotel in instance.hotels.all()] if instance.hotels.exists() else []

    tourist_place_name = serializers.CharField(source='tourist_place.name', read_only=True)

    class Meta:
        model = TourPackage
        fields = ['id', 'name' , 'description' , 'number_of_days', 'number_of_nights', 'tourist_place', 'hotels' , 'hotel_name', 'tourist_place_name', 'price']


class HotelSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'pincode', 'state', 'district', 'contact_no', 'state_name', 'district_name']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class TouristPlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristPlaceImage
        fields = ['id', 'image', 'caption']

class TouristPlaceSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    images = TouristPlaceImageSerializer(many=True, read_only=True)  # Include the nested serializer

    class Meta:
        model = TouristPlace
        fields = ['id', 'name', 'description', 'location_link', 'address', 'pincode', 'state', 'district', 'state_name', 'district_name', 'images']


from .models import DiscountCode

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'
