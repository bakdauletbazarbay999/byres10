from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from calculator import views


urlpatterns = [
    path('', views.index, name='index'),
    path('lab1/', views.lab1, name='lab1'),
    path('lab2/<str:Item>', views.lab2, name="lab2"),
    path('lab2/', views.lab2, name="lab2"),
    path('lab3/', views.lab3, name="lab3"),
    path('lab4/', views.lab4, name='lab4'),
    path('soj/', views.soj, name='soj'),
    path('lab5_1/', views.lab5_1, name='lab5_1'),
    path('lab5_2', views.lab5_2, name='lab5_2'),
    path('lab6/', views.lab6, name='lab6'),
    path("lab7/", views.lab7, name="lab7"),
    path("lab7/result/", views.lab7_result, name="lab7_result"),
    path("lab7/tapsyrma/", views.lab7_tapsyrma, name="lab7_tapsyrma"),
    path('admin/', admin.site.urls),
    path('chat', views.chat_view, name='chat_home'),
    path('clear/', views.clear_history, name='clear_history'),
    path('history/', views.history_view, name='full_history'),
    path('index6', views.index6, name='index6'),
    path('menu/', views.menu_list, name='menu'),
    path('menu/<slug:category_slug>/', views.menu_list, name='menu_by_category'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/change_qty/', views.change_cart_item_quantity, name='change_cart_item_quantity'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='my_orders'),
    path('director/', views.director_dashboard, name='director_dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='calculator/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='calculator/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('add-one/<int:dish_id>/', views.quick_add_to_cart, name='quick_add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('director/change_status/<int:order_id>/<str:new_status>/', views.change_order_status, name='change_order_status'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='calculator/password_change.html',success_url='/profile/'), name='password_change'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)