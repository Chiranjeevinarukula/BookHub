"""
URL configuration for BookHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView
from userProfile import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeView
from django.urls import path,reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('books/',include('books.urls')),
    path('profile/<int:pk>/',views.profileView,name='profile'),
    path('profile/edit/',views.ProfileUpdateView.as_view(),name='profileUpdate'),
    path('profile/change_password/', PasswordChangeView.as_view(template_name='account/change_password.html',success_url=reverse_lazy('password_change_done')), name='change_password'),
    path('profile/password_change_done/', views.password_change_done, name='password_change_done'),
    path('<int:userId>/block',views.blockUser,name='blockUser'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
