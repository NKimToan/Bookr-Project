"""
URL configuration for bookr project.

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
from django.urls import path, include
import reviews.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import auth
from bookr.views import profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
    path("book-search/", reviews.views.book_search),
    path('accounts/',
         include(("django.contrib.auth.urls", "auth"),
            namespace="accounts")
         ), # Truy cập django.contrib.auth.urls để xem các urlpatterns trong đó
    path("accounts/password_reset/done/",
         auth.views.PasswordResetDoneView.as_view(),
         name="password_reset_done",
         ),
    path("accounts/reset/done/",
         auth.views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete",
         ),
    path("accounts/profile/", profile, name='profile') #Notice
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)