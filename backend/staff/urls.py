from rest_framework.routers import SimpleRouter
from .views import AssessorViewSet, HelperViewSet


router = SimpleRouter(trailing_slash=True)
router.register(r'assessors', AssessorViewSet, 'assessor')
router.register(r'helpers', HelperViewSet, 'helper')

urlpatterns = router.urls
