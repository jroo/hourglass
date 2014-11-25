from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PaginatedContractSerializer
from contracts.models import Contract

class GetRates(APIView):

    def get(self, request, format=None):
       
        page = 1

        contracts = self.get_queryset()
        paginator = Paginator(contracts, 20)
        contracts = paginator.page(page)

        serializer = PaginatedContractSerializer(contracts)
        return Response(serializer.data)


    def get_queryset(self): 
       contracts = Contract.objects.all()
       return contracts
