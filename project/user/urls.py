from django.urls import path
from .views import BuyerView, VendorView, MyOwnLogoutView, AddProfileView, ProfileListView,OrderView
# ProfileView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views

app_name = 'user'

urlpatterns = [
    path('vendor_reg/', VendorView.as_view(), name='vendor_reg'),
    path('buyer_reg/', BuyerView.as_view(), name='buyer_reg'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('add_profile/', AddProfileView.as_view(), name='add_profile'),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', MyOwnLogoutView.as_view(), name='logout'),
]
