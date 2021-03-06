"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from account.api.views import BankAccountViewSet
from account.views import HomePage
from card.api.views import CardViewSet
from transfer.api.views import TransferViewSet


schema_view = get_schema_view(
   openapi.Info(
      title="Bank API",
      default_version='v1',
      description="RESTful API for Bank.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', HomePage.as_view(), name='index'),
    path('account/', include('account.urls', namespace='account')),
    path('transfer/', include('transfer.urls', namespace='transfer')),
    path('card/', include('card.urls', namespace='card'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


router = routers.DefaultRouter()
router.register('bank-accounts', BankAccountViewSet, 'bank-account')
router.register('transfers', TransferViewSet, 'transfer')
router.register('cards', CardViewSet, 'card')

urlpatterns_api = [
    path('api/', include(router.urls)),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += urlpatterns_api

handler404 = 'account.views.custom_page_not_found'
handler500 = 'account.views.custom_server_error'
handler403 = 'account.views.custom_permission_denied'
handler400 = 'account.views.custom_bad_request'
