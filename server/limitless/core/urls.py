from dj_rest_auth import views as rest_auth_views
from django.conf import settings
from django.urls import include, path
from rest_framework_nested import routers

from limitless.core import views as core_views
from limitless.projects import views as project_views

router = routers.SimpleRouter()
if settings.DEBUG:
    router = routers.DefaultRouter()

router.register("users", core_views.UserViewSet)
router.register("projects", project_views.ProjectViewSet)

urlpatterns = [
    path(r"api/projects/print/", project_views.print),
    path("api/", include(router.urls)),
    path("api/login/", core_views.UserLoginView.as_view()),
    path(r"api/logout/", rest_auth_views.LogoutView.as_view()),
    path(r"api/password/reset/confirm/<str:uid>/<str:token>/", core_views.reset_password, name="password_reset_confirm"),
    path(r"api/password/reset/", core_views.request_reset_link),
    path(r"api/password/change/", rest_auth_views.PasswordChangeView.as_view()),
    path(r"api/template_preview/", core_views.PreviewTemplateView.as_view()),
]
