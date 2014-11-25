from contracts.models import Contract
from rest_framework import serializers, pagination

class ContractSerializer(serializers.ModelSerializer):

    education_level = serializers.Field(source='get_education_level_display')

    class Meta:
        model = Contract
        fields = ('idv_piid', 'vendor_name', 'labor_category', 'education_level', 'min_years_experience', 'hourly_rate_year1')

class PaginatedContractSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = ContractSerializer
