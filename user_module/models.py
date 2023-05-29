from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission

from admin_module.models import TouristPlace, Hotel, DiscountCode

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=240)
    dob = models.DateField(null=True, blank=True)
    contact_no = models.CharField(max_length=12, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    photo = models.ImageField(upload_to='user_photos', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='user_profiles', verbose_name=_('groups'), blank=True,
                                    help_text=_('The groups this user belongs to. A user will get all permissions '
                                                'granted to each of their groups.'))

    user_permissions = models.ManyToManyField(Permission, related_name='user_profiles', verbose_name=_('user permissions'),
                                               blank=True, help_text=_('Specific permissions for this user.'))

    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class TourPackage(models.Model):
    name = models.CharField(max_length=100)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='user_tour_packages')
    hotels = models.ManyToManyField(Hotel, related_name='user_tour_packages')
    tourist_places = models.ManyToManyField(TouristPlace, related_name='user_tour_packages')
    number_of_days = models.PositiveIntegerField(default=0)
    number_of_nights = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'user_tour_package'


class Booking(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    tour_package = models.ForeignKey('admin_module.TourPackage', on_delete=models.CASCADE)
    book_date = models.DateField()
    contact_number = models.CharField(max_length=15)
    payment_screenshot = models.ImageField(upload_to="booking/payment_screenshots", null=True)
    payment_approved = models.BooleanField(default=False)
    num_rooms = models.PositiveIntegerField(default=0)
    num_adults = models.PositiveIntegerField(default=0)
    num_children = models.PositiveIntegerField(default=0)
    discountcode = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_rejected = models.BooleanField(default=False)

    class Meta:
        db_table = "booking"



class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "invoice"