from rest_framework.routers import DefaultRouter
from .views import SubjectsViewSet

router = DefaultRouter()
router.register("subjects", SubjectsViewSet, basename="subject")
urlpatterns = router.urls