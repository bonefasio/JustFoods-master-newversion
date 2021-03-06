"""e_food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

admin.site.site_header = "JustFoods Admin"
admin.site.site_title = "JustFoods"
admin.site.index_title = "JustFoods Administration Panel"

urlpatterns = [
    path('admin/', admin.site.urls),

    # rest api urls
    path('auth/', obtain_auth_token),
    path('api/', include('api.urls')),


    # web applications urls
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('mealsubscription/', include('mealsubscription.urls')),
    path('stripepayment/', include('stripepayment.urls')),
    path('staff/', include('staff.urls')),
    path('mealmenu/', include('mealmenu.urls')),
    path('payrollpayment/', include('payrollpayment.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
