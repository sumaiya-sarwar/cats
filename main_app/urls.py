from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('cats/', views.CatList.as_view(), name="cat_list"),
    path('cats/new/', views.CatCreate.as_view(), name="cat_create"),
     path('cats/<int:pk>/', views.CatDetail.as_view(), name="cat_detail"),
    path('cats/<int:pk>/update',views.CatUpdate.as_view(), name="cat_update"),
    path('cats/<int:pk>/delete',views.CatDelete.as_view(), name="cat_delete"),
    path('accounts/signup/', views.Signup.as_view(), name="signup")

]