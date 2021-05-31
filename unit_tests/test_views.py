'''
from django.test import TestCase, Client
from django.urls import reverse
from main.models import *  # import all tables from models
import json


class TestViews(TestCase):
    # going to run before every test method
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('main:home')
        self.dishes_url = reverse('main:dishes', args=['item1'])
        self.user1 = User.objects.create()
        self.item1 = Item.objects.create(
            title='Curry Dhal',
            description='Available for Pickup',
            price=12,
            instructions='Deliver',
            image='',
            labels='',
            label_colour='',
            slug='currydhal',
            # created_by=self.user,
            quantity_available=20,
            subcription_avail=True
        )

    def test_MenuListView_GET(self):
        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_menuDetail_GET(self):
        response = self.client.get(self.dishes_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/dishes.html')
    
    def test_menuDetail_GET(self):
        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/dishes.html')
    '''
