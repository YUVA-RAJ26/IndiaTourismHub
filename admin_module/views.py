from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import TourPackage, Hotel, TouristPlace, State, District, DiscountCode, TouristPlaceImage
from .serializers import TourPackageSerializer, HotelSerializer, TouristPlaceSerializer, StateSerializer, DistrictSerializer, DiscountCodeSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
import pdfkit
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from reportlab.pdfgen import canvas

#Start Of Listing Pages HTML Code
@login_required
def hotel_list(request):
    token = Token.objects.get(user=request.user)
    context = {'authToken': f'Token {str(token)}'}
    return render(request, 'admin_module/hotel_list.html', context)

@login_required
def state_list(request):
    states = State.objects.all()
    return render(request, 'admin_module/state_list.html')

@login_required
def district_list(request):
    states = District.objects.all()
    return render(request, 'admin_module/state_list.html')

def tour_package_list(request):
    token = Token.objects.get(user=request.user)
    tourist_place_id = request.GET.get('touristPlaceId')  
    context = {
        'authToken': f'Token {str(token)}',
        'touristPlaceId': tourist_place_id  
    }
    return render(request, 'admin_module/tour_package_list.html', context)

@login_required
def tourist_place_list(request):
    tourist_places = TouristPlace.objects.all()
    token = Token.objects.get(user=request.user)
    states = State.objects.all()
    districts = District.objects.all()
    context = {
        'authToken': f'Token {str(token)}',
        'states': states,
        'districts': districts,
        'tourist_places': tourist_places
    }
    return render(request, 'admin_module/tourist_place_list.html', context)

def create_tourist_place(request):
    token = Token.objects.get(user=request.user)
    context = {'authToken': f'Token {str(token)}'}
    return render(request, 'admin_module/create-tourist.html', context) 

def download_tour_packages_pdf(request):
    tour_packages = TourPackage.objects.all()

    # Create a response object with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tour_packages.pdf"'

    # Create the PDF document
    p = canvas.Canvas(response)

    # Set up the font and size
    p.setFont("Helvetica", 12)

    # Write the tour package details to the PDF
    y = 750
    for tour_package in tour_packages:
        p.drawString(50, y, f"Name: {tour_package.name}")
        p.drawString(50, y - 20, f"Description: {tour_package.description}")
        p.drawString(50, y - 40, f"Price: {tour_package.price}")
        p.drawString(50, y - 60, "Hotels: ")
        
        hotel_names = ", ".join([hotel.name for hotel in tour_package.hotels.all()])
        p.drawString(120, y - 60, hotel_names)
        
        p.drawString(50, y - 80, f"Number of Days: {tour_package.number_of_days}")
        p.drawString(50, y - 100, f"Number of Nights: {tour_package.number_of_nights}")
        # Add more fields if needed

        y -= 160  # Adjust the space between each tourist package

    p.showPage()
    p.save()

    return response

#Start Of Class Based Views
class TourPackageViewSet(viewsets.ModelViewSet):
    queryset = TourPackage.objects.all()
    serializer_class = TourPackageSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        headers = {'Authorization': f'Token {request.auth}'}
        tourist_place_id = request.GET.get('touristPlaceId')
        queryset = TourPackage.objects.all()

        if tourist_place_id and tourist_place_id != 'None':
            queryset = queryset.filter(tourist_place_id=tourist_place_id)    
    
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_serializer(page, many=True)
            return self.get_paginated_response(paginated_data.data)
        tour_package_data = self.get_serializer(queryset, many=True)
        return Response(tour_package_data.data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {'message': 'Tour package deleted successfully'}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        headers = {'Authorization': f'Token {request.auth}'}
        queryset = Hotel.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_serializer(page, many=True)
            return self.get_paginated_response(paginated_data.data)
        hotel_data = self.get_serializer(queryset, many=True)
        return Response(hotel_data.data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {'message': 'Hotel deleted successfully'}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

class TouristPlaceViewSet(viewsets.ModelViewSet):
    queryset = TouristPlace.objects.all()
    serializer_class = TouristPlaceSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def list(self, request):
        headers = {'Authorization': f'Token {request.auth}'}
        queryset = TouristPlace.objects.all()

        state = request.GET.get('state')
        district = request.GET.get('district')
        search_query = request.GET.get('search')
        
        # Apply filters to the queryset
        if state:
            queryset = queryset.filter(state_id=state)
        if district:
            queryset = queryset.filter(district_id=district)

        # Perform the search based on tourist name or pincode
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(pincode__icontains=search_query)
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_serializer(page, many=True)
            return self.get_paginated_response(paginated_data.data)
        
        # Serialize the filtered queryset
        tourist_place_data = self.get_serializer(queryset, many=True)
        return Response(tourist_place_data.data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        images_data = request.FILES.getlist('images')  # Retrieve the list of uploaded images
        for image_data in images_data:
            TouristPlaceImage.objects.create(
                tourist_place=serializer.instance,
                image=image_data,
                caption='Caption for the image'  # Provide a caption for the image
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {'message': 'Tourist place deleted successfully'}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    pagination_class = LimitOffsetPagination


    def list(self, request):
        headers = {'Authorization': f'Token {request.auth}'}
        queryset = State.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_serializer(page, many=True)
            return self.get_paginated_response(paginated_data.data)
        tourist_place_data = self.get_serializer(queryset, many=True)
        return Response(tourist_place_data.data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {'message': 'State deleted successfully'}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    pagination_class = LimitOffsetPagination


    def list(self, request):
        headers = {'Authorization': f'Token {request.auth}'}
        queryset = District.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_serializer(page, many=True)
            return self.get_paginated_response(paginated_data.data)
        tourist_place_data = self.get_serializer(queryset, many=True)
        return Response(tourist_place_data.data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {'message': 'District deleted successfully'}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], url_path="get_state_districts", url_name="get_state_districts")
    def get_state_districts(self, request, state_id):
        districts = District.objects.filter(state_id=state_id).values('id', 'name')
        return Response(districts)

    @action(detail=False, methods=["GET"], url_path="get_pincode_state_districts", url_name="get_pincode_state_districts")
    def get_pincode_state_districts(self, request):
        pincode = request.GET.get('pincode')
        districts = District.objects.filter(pincode=pincode).values('id', 'name', 'state_id')
        return Response(districts)
        
class DiscountCodeViewSet(viewsets.ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer

    def list(self, request):
        headers = {'Authorization': f'Token {request.auth}'}
        code = request.GET.get('code')
        queryset = DiscountCode.objects.all()

        if code:
            queryset = queryset.filter(code=code)    
    
        discountcode_data = self.get_serializer(queryset, many=True)
        return Response(discountcode_data.data, status=status.HTTP_200_OK, headers=headers)









