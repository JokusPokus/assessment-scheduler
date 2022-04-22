from rest_framework.routers import SimpleRouter
from .views import AssessorViewSet


router = SimpleRouter(trailing_slash=True)
router.register(r'assessors', AssessorViewSet, 'assessor')

urlpatterns = router.urls
