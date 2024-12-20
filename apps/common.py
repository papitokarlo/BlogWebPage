from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class PaginationClass(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
