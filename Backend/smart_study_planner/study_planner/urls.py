from rest_framework.routers import DefaultRouter
from study_planner.views import StudyPlannerViewSet

router = DefaultRouter()
router.register("study_planner", StudyPlannerViewSet, basename="study-planner")
urlpatterns = router.urls