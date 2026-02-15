from django.urls import path
from users.views import RegisterUserView, TokenObtainPair, TokenRefresh, LogoutUserView, DeleteUserView
from users import views

urlpatterns = [
    path('register/', RegisterUserView.as_view(),),
    path('token/', TokenObtainPair.as_view(),),
    path('token/refresh/', TokenRefresh.as_view()),
    path('logout/', LogoutUserView.as_view(),),
    path('delete/<int:id>/', DeleteUserView.as_view(),),
]