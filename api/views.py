from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Avg, Max, Min

from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PaginatedContractSerializer
from contracts.models import Contract, EDUCATION_CHOICES

class GetRates(APIView):

    def get(self, request, format=None):
       
        page = request.QUERY_PARAMS.get('page', 1)
        contracts_all = self.get_queryset(request)

        wage_field = 'hourly_rate_year1'

        paginator = Paginator(contracts_all, settings.PAGINATION)
        contracts = paginator.page(page)

        serializer = PaginatedContractSerializer(contracts)

        serializer.data['average'] = "{0:.2f}".format(contracts_all.aggregate(Avg(wage_field))[wage_field + '__avg'])
        serializer.data['minimum'] = contracts_all.aggregate(Min(wage_field))[wage_field + '__min']
        serializer.data['maximum'] = contracts_all.aggregate(Max(wage_field))[wage_field + '__max']

        hourly_wage_stats = contracts_all.values('min_years_experience').annotate(average_wage=Avg(wage_field), min_wage=Min(wage_field), max_wage=Max(wage_field))

        #Avg always returns float, so make it a fixed point string in each dict
        for item in hourly_wage_stats:
            item['average_wage'] = "{0:.2f}".format(item['average_wage'])

        serializer.data['hourly_wage_stats'] = sorted(hourly_wage_stats, key=lambda mye: mye['min_years_experience'])

        return Response(serializer.data)


    def get_queryset(self, request):

        query = request.QUERY_PARAMS.get('q', None)
        min_experience = request.QUERY_PARAMS.get('min_experience', 0)
        max_experience = request.QUERY_PARAMS.get('max_experience', 100)
        min_education = request.QUERY_PARAMS.get('min_education', None)

        contracts = Contract.objects.filter(min_years_experience__gte=min_experience, min_years_experience__lte=max_experience)

        if query:
            contracts = contracts.search(query, raw=True)

        if min_education:
            for index, pair in enumerate(EDUCATION_CHOICES):
                if min_education == pair[0]:
                    contracts = contracts.filter(education_level__in=[ed[0] for ed in EDUCATION_CHOICES[index:] ])

        return contracts
