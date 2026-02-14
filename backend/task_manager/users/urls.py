from django.urls import path
from users.views import RegisterUserView, LoginUserView, LogoutUserView, DeleteUserView
from users import views

urlpatterns = [
    path('register/', RegisterUserView.as_view(),),
    path('login/', LoginUserView.as_view(),),
    path('logout/', LogoutUserView.as_view(),),
    # path('me/', views.get_user,),
    path('delete/<int:id>/', DeleteUserView.as_view(),)
]