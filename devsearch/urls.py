import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/', include('api.urls')),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 1 - User submits email for reset              // PasswordResetView.as_view()
# 2 - Email send message                        // PasswordResetDoneView.as_view()
# 3 - Email with Link and reset instruction     // PasswordResetConfirmView.as_view()
# 4 - Password successfully reset message       // PasswordResetCompleteView.as_view()