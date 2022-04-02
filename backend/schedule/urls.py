from rest_framework.routers import SimpleRouter
from .views import AssessmentPhaseViewSet, WindowViewSet


router = SimpleRouter(trailing_slash=True)
router.register(r'assessment-phases', AssessmentPhaseViewSet, 'assessment-phase')
router.register(r'windows', WindowViewSet, 'window')

urlpatterns = router.urls
