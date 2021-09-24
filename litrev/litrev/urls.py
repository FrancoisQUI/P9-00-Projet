"""litrev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
                  path('', views.index, name="site-index"),
                  path('signup/', views.sign_up, name="sign-up"),
                  path('disconnect/', views.disconnect, name="disconnect"),
                  path('feed/', views.feed, name="feed"),
                  path('post/', views.post, name="post"),
                  path('subs/', views.subs, name="subs"),
                  path('rev/', include('bkreport.urls')),
                  path('admin/', admin.site.urls),
              ] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
