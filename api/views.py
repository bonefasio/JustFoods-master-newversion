from django.db.models.query import QuerySet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from main.models import *  # import all models
from .serializers import *  # import all serializer
from .serializers import CustomerSerializer, ItemSerializer, MealSubscriptionSerializer, PayrollSerializer, UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def order_item(self, request, pk=None):
        if 'fooditem' in request.data:

            item = Item.objects.get(id=pk)
            #stars = request.data['stars']
            user = request.user.customer
           # customer = request.user.customer

            try:
                order = OrderItems.objects.get(customer=user.id, item=item.id)
                order.save()
                serializer = OrderItemsSerializer(order, many=False)
                response = {'message': 'Ordered Items sucessfuly',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                order = OrderItems.objects.create(
                    customer=user, item=item)
                serializer = OrderItemsSerializer(order, many=False)
                response = {'message': 'Order created',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'You need to place on order'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)


class PaidOrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return OrderItems.objects.filter()


class MealSubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = MealSubscription.objects.all()
    serializer_class = MealSubscriptionSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['GET'])
    def location(self, request, pk=None):
        if 'offsite' in request.data:
            # offsite = Location.objects.get(id=pk)
            offsite = Location.objects.get(id=pk, category='OnSite')
            offsite.save()
            serializer = LocationSerializer(offsite, many=True)
            response = {'message': 'Onsite',
                        'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        elif 'onsite' in request.data:
            onsite = Location.objects.get(id=pk, category='OnSite')
            onsite.save()
            serializer = LocationSerializer(onsite, many=True)
            response = {'message': 'Ordered Items sucessfuly',
                        'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'No Locations available'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)


class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)


''' 
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:

            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(
                    user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
'''
