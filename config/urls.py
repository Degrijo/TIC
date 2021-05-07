"""config URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app.core.views import SignUpClientView, LogInView, MainPageView, SignUpEmployeeView, CreateOrderView, \
    ListMyOrdersView, LogOutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_page/', MainPageView.as_view(), name='main_page'),
    path('signup_client/', SignUpClientView.as_view(), name='signup_client'),
    path('signup_employee/', SignUpEmployeeView.as_view(), name='signup_employee'),
    path('login/', LogInView.as_view(), name='login'),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('list_my_orders/', ListMyOrdersView.as_view(), name='list_my_orders'),
    path('logout/', LogOutView.as_view(), name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
