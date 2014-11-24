from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from contracts.models import Contract
import csv
import os

class Command(BaseCommand):

    def handle(self, *args, **options):

        data_file = csv.reader(open(os.path.join(settings.BASE_DIR, 'contracts/docs/hourly_prices.csv'), 'r'))
        #skip header row
        next(data_file)
        
        for line in data_file:
            
            if line[0]:
                #create contract record, unique to vendor, labor cat
                print(line)
                idv_piid = line[0]
                vendor_name = line[1]
                labor_category = line[2]
                
                try:
                    contract = Contract.objects.get(idv_piid=idv_piid, labor_category=labor_category, vendor_name=vendor_name)
                
                except Contract.DoesNotExist:
                    contract = Contract()
                    contract.idv_piid = idv_piid
                    contract.labor_category = labor_category
                    contract.vendor_name = vendor_name

                contract.education_level = contract.get_education_code(line[3])
                
                if line[4].strip() != '':
                    contract.min_years_experience = line[4]
                else:
                    contract.min_years_experience = 0

                if line[5] and line[5] != '': 
                    contract.hourly_rate_year1 = contract.normalize_rate(line[5])
                else:
                    #there's no pricing info
                    continue
                
                for count, rate in enumerate(line[6:10]):
                    if rate and rate.strip() != '':
                        setattr(contract, 'hourly_rate_year' + str(count+2), contract.normalize_rate(rate))
                
                
                #contract.hourly_rate_year3 = line[7]
                #contract.hourly_rate_year4 = line[8]
                #contract.hourly_rate_year5 = line[9]
                contract.contractor_site = line[10]

                contract.save()

