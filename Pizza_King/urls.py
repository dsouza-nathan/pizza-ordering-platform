from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from myapp import views  # Correct import path

urlpatterns = [
    path('', views.home, name='home'),  # Set home as the root URL
    path('menu/', views.menu, name='menu'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.register_page, name='signup'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders, name='orders'),
    path('add-to-cart/<str:pizza_uid>/', views.add_cart, name='add_cart'),
    path('remove-from-cart/<str:cart_item_uid>/', views.remove_cart_items, name='remove_cart_items'),
    path('home/', views.home, name='home'),  # Optional: explicit home path for clarity
    path('admin/', admin.site.urls),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
