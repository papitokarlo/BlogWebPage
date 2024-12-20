from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentViewSet, TagViewSet, MenuViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = router.urls
