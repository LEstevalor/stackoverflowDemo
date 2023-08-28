from django.urls import re_path, path
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import users, questions

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 登录注册
    re_path(r'^api/v1/user/login/$', users.LoginTokenView.as_view(), name='token_obtain_pair'),  # JWT登录功能
    re_path(r'^api/v1/user/register/$', users.RegisterUserView.as_view()),  # 注册功能
]

router = DefaultRouter()
router.register("api/v1/users", users.UserViewSet)
router.register("api/v1/questions", questions.QuestionViewSet)

urlpatterns += router.urls

# swagger
urlpatterns += [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json")
]
