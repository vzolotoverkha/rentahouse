from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rentservice.models import Apartment, City, Street
from rentservice.serializers import ApartmentSerializer, CitySerializer, StreetSerializer, CityDetailSerializer, \
    ApartmentDetailSerializer


class CityList(APIView):
    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CityDetail(APIView):
    def get(self, request, city_id):
        city = City.objects.filter(id=city_id).first()

        if not city:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        streets = Street.objects.filter(city__id=city_id).all()
        streets_list = [
            {'id': street.id, 'name': street.name, 'street_number': street.street_number} for street in streets
        ]
        response = {'city_name': city.name, 'streets_list': streets_list}
        serializer = CityDetailSerializer(data=response)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, city_id):
        city = City.objects.filter(id=city_id).first()

        if not city:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = StreetSerializer(data=request.data)
        if serializer.is_valid():
            Street.objects.create(city=city, name=serializer.data.get('name'),
                                  street_number=serializer.data.get('street_number'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class ApartmentDetail(APIView):

    def apartments_list(self, street_id):
        street_apartments = list(Apartment.objects.select_related().filter(street__id=street_id).values())
        return street_apartments

    def get(self, request, city_id):
        city = City.objects.filter(id=city_id).first()

        if not city:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        streets = Street.objects.filter(city__id=city_id)
        apartment_data = []
        for street in streets:
            apartment_list = Apartment.objects.filter(city__id=city_id, street__id=street.id).all()
            apt_details = [{'id': item.id, 'price': item.price} for item in apartment_list]
            apartment_data.append({'street_name': street.name, 'apartments': apt_details})

        serializer = ApartmentDetailSerializer(data=apartment_data, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, city_id):
        city = City.objects.filter(id=city_id).first()
        street = Street.objects.filter(name=request.data['street'], city__id=city_id).first()

        if not street or not city:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ApartmentSerializer(data=request.data)
        if serializer.is_valid():
            Apartment.objects.create(city=city, street=street,
                                     price=serializer.data.get('price'),
                                     area=serializer.data.get('area'),
                                     rooms=serializer.data.get('rooms'),
                                     floor=serializer.data.get('floor'),
                                     free=serializer.data.get('free'),
                                     width=serializer.data.get('width'),
                                     length=serializer.data.get('length'))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApartmentFilter(APIView):
    def get(self, request):
        all_apts = Apartment.objects.all()
        print(f"ALL {all_apts}")
        price = request.query_params.get('price', None)
        print(price)
        width = request.query_params.get('width', None)
        #
        # if price:
        #     filtered = all_apts.filter(price=price)
        #     print(f"PRICED {filtered}")
        # if width:
        #     filtered = all_apts.filter(width=width)
        #     print(f"WIDTHED {filtered}")

        # if price is not None and width is not None:
        filtered = all_apts.filter(price__gt=price, width__gt=width)
        print(f"PRICED AND WIDTHED {filtered}")






        """
        example url: http://127.0.0.1:8000/apartment?city=Kiev&street=Kovalivska
        your url: http://127.0.0.1:8000/apartment?price=2000&width=100
        вернуть все квартиры в которых price > указанного в url
        """
        params = request.query_params  # возращается дикт параметров - которые в урл после знака ? (& - и){'city': ['Kiev'], 'street': ['Kovalivska']}
        print(params)
        return Response({}, status=status.HTTP_200_OK)
