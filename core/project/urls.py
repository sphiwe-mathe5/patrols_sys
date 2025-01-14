from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core.project.settings import ADMIN_PATH
from core.views import index, ResidentCreateView, ResidentListView, PaymentActionView, ResidentDeleteView


urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('', include('submit.urls')),
    path('resident/new/', ResidentCreateView.as_view(), name='create_resident'),
    path('residents/', ResidentListView.as_view(), name='resident_list'),
    path('resident/<int:payment_id>/mark-paid/', PaymentActionView.as_view(), name='mark_as_paid'),
    path('resident/<int:resident_id>/delete/', ResidentDeleteView.as_view(), name='delete_resident'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='submit/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='submit/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='submit/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='submit/password_reset_complete.html'),
         name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
