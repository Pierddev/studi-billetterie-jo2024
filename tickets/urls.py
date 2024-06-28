from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('tickets', views.tickets_list, name='tickets_list'),
    path('add_to_cart/<int:ticket_id>/', views.add_to_cart, name='add_to_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    # Stripe
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.success_view, name='success'),
    path('cancelled/', views.cancelled_view, name='cancelled'),
    path('webhook/', views.stripe_webhook, name="stripe_webhook"),
    # User
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('qr_code/<int:purchase_id>/', views.view_qr_code, name='view_qr_code'),
    # Administration
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('delete_ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
]
