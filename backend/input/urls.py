from rest_framework.routers import SimpleRouter
from .views import PlanningSheetView


router = SimpleRouter(trailing_slash=True)
router.register(r'planning-sheets', PlanningSheetView, 'input-planning-sheet')

urlpatterns = router.urls
