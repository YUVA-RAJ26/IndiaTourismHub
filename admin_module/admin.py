from django.contrib import admin
from .models import TourPackage, Hotel, TouristPlace, State, District, DiscountCode, TouristPlaceImage

admin.site.register(State)
admin.site.register(District)
admin.site.register(TouristPlace)
admin.site.register(TourPackage)
admin.site.register(Hotel)
admin.site.register(DiscountCode)
admin.site.register(TouristPlaceImage)