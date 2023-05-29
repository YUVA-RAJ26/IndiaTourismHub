from django.db import models


class TouristPlace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location_link = models.URLField()
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tourist_place'


class State(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'state'


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10, default='000000')

    class Meta:
        db_table = 'district'


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        db_table = 'hotel'


class DiscountCode(models.Model):
    code = models.CharField(max_length=50)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'discount_code'


class TourPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='admin_tour_packages')
    hotels = models.ManyToManyField(Hotel, related_name='admin_tour_packages')
    tourist_place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE)
    number_of_days = models.PositiveIntegerField(default=0)
    number_of_nights = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'admin_tour_package'

class TouristPlaceImage(models.Model):
    tourist_place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tourist_place_images')
    caption = models.CharField(max_length=100)

    class Meta:
        db_table = 'tourist_place_image'
