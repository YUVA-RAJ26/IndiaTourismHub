from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    tour_package_name = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_name', 'tour_package', 'tour_package_name', 'book_date', 'contact_number',
                  'payment_screenshot', 'payment_approved', 'num_rooms', 'num_adults', 'num_children', 'discountcode',
                  'price', 'payment_rejected']

    def get_user_name(self, obj):
        return obj.user.username

    def get_tour_package_name(self, obj):
        return obj.tour_package.name
