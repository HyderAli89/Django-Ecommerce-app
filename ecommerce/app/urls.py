from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm, MyPasswordChangeForm
from django.contrib import admin


urlpatterns = [
    path("",views.home),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path("category/<slug:val>",views.CategoryView.as_view(),name='category'),
    path("category-title/<val>",views.CategoryTitle.as_view(),name='category-title'),
    path("product-detail/<int:pk>",views.ProductDetails.as_view(),name='product-detail'),
    path("profile/", views.ProfileView.as_view(),name='profile'),
    path("address/", views.address,name='address'),
    path("updateAddress/<int:pk>",views.updateAddress.as_view(), name='updateAddress'),
   
    # CART - SECTION    
    path('add-to-cart/', views.add_to_cart , name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'), 
    path("checkout/",views.checkout.as_view(),name='checkout'),
    path('paymentdone/',views.payment_done, name='paymentdone'),
    path("orders/", views.orders, name="orders"),
    path("shop/", views.home),
   
    # wishlist
    path('wishlist',views.show_wishlist,name='showwishlist'),
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),
    
    path("pluscart/",views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('search/',views.search,name="search"),

    # user authentication 
    path('customerregistration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
   # path("password_reset",auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordChangeForm),name='password_reset'),
    path('changepassword/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='changepassword'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    
]+static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)  # to access media/images folder


admin.site.site_header = "NEEL DAIRY"
admin.site.site_title = "NEEL DAIRY"
admin.site.site_index_title = "WELCOME TO  NEEL DAIRY AN E-COMMERCE SHOP" 