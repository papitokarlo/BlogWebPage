from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Blog, Comment, Tag, Menu, Category
from .serializers import (
    BlogSerializer,
    CommentSerializer,
    TagSerializer,
    MenuSerializer,
    CategorySerializer
)


class PaginationClass(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = PaginationClass
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author', 'category', 'tags', 'active']
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Blog.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            instance.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "You cant delete this Blog"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            serializer_data = self.serializer_class(instance, data=request.data, partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response(serializer_data.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You cant delete this Blog"}, status=status.HTTP_403_FORBIDDEN)


class CommentViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PaginationClass
    filterset_fields = ['blog']

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_id = self.request.query_params.get('blog')
        if blog_id:
            return Comment.objects.filter(blog=blog_id)
        return self.queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            instance.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "You cant delete this comment"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            serializer_data = self.serializer_class(instance, data=request.data, partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response(serializer_data.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You cant delete this comment"}, status=status.HTTP_403_FORBIDDEN)


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MenuViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

