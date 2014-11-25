from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PaginatedContractSerializer
from contracts.models import Contract

class GetRates(APIView):

    def get(self, request, format=None):
       
        page = request.QUERY_PARAMS.get('page', 1)
        query = request.QUERY_PARAMS.get('q', None)

        contracts = self.get_queryset(query=query)
        paginator = Paginator(contracts, settings.PAGINATION)
        contracts = paginator.page(page)

        serializer = PaginatedContractSerializer(contracts)
        return Response(serializer.data)


    def get_queryset(self, query=None):
        
        contracts = Contract.objects.all()
        if query:
            contracts = contracts.search(query, raw=True)
        return contracts
