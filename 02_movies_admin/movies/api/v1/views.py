from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_queryset(self):
        return self.model.objects.all()

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

class MoviesListApi(MoviesApiMixin, BaseListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        context = {
            'count': paginator.count,
            'total_pages': page.paginator.num_pages,
            'next': page.next_page_number() if page.has_next() else None,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'results': list(queryset.values()),
        }
        return context 

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = {
            'count': 1,
            'total_pages': 1,
            'next': None,
            'prev': None,
            'results': [obj]  # Объект в списке для единого формата
        }
        return context