from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        cache_key = f'faq_list_{lang}'
        cached_data = cache.get(cache_key)

        if cached_data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True, context={'lang': lang})
            data = serializer.data
            cache.set(cache_key, data, timeout=settings.CACHE_TIMEOUT)
        else:
            data = cached_data

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'lang': lang})
        return Response(serializer.data)

