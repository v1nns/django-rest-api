"""restserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from services import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
router.register(r'checkouts', views.CheckoutViewSet)
router.register(r'payments', views.PaymentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^/', include(router.urls)),
    url(r'^requestPayment/', views.requestPayment),
    url(r'^getPaymentRequests/', views.getPaymentRequests),
	url(r'^getPaymentRequest/(?P<checkout>[0-9]+)$', views.getPaymentRequest),
    url(r'^removeCheckouts/', views.removeCheckouts),
    url(r'^removePaymentRequests/', views.removePaymentRequests),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]