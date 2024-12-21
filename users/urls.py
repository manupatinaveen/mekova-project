from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserUpdateView, UserGroupAssignmentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('assign-group/', UserGroupAssignmentView.as_view(), name='assign_group'),
    

]
