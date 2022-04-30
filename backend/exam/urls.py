from rest_framework.routers import SimpleRouter
from .views import ModuleViewSet


router = SimpleRouter(trailing_slash=True)
router.register(r'modules', ModuleViewSet, 'module')

urlpatterns = router.urls
