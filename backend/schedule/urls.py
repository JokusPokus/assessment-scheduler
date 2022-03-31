from rest_framework.routers import SimpleRouter
from .views import AssessmentPhaseViewSet


router = SimpleRouter(trailing_slash=True)
router.register(r'assessment-phases', AssessmentPhaseViewSet, 'assessment-phase')

urlpatterns = router.urls
