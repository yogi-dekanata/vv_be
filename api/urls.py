from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.get_products, name='products'),
    path('categories/', views.list_categories, name='list_categories'),
    path('search-products/', views.search_products, name='search_products'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

]
