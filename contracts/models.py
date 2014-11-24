from django.db import models
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField


EDUCATION_CHOICES = (
    ('HS', 'High School'),
    ('BA', 'Bachelors'),
    ('MA', 'Masters'),
    ('AA', 'Associates'),
    ('PHD', 'Ph.D.'),
)


class Contract(models.Model):

    idv_piid = models.CharField(max_length=128) #index this field
    piid = models.CharField(max_length=128) #index this field
    vendor_name = models.CharField(max_length=128)
    labor_category = models.TextField() #index this field
    education_level = models.CharField(choices=EDUCATION_CHOICES, max_length=5, null=True, blank=True)
    min_years_experience = models.IntegerField()
    hourly_rate_year1 = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate_year2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hourly_rate_year3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hourly_rate_year4 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hourly_rate_year5 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contractor_site = models.CharField(max_length=128, null=True, blank=True)

    search_index = VectorField()

    objects = SearchManager(
        fields=('labor_category',),
        config = 'pg_catalog.english',
        search_field='search_index',
        auto_update_search_field = True
    )


    def get_education_code(self, text):
        
        for pair in EDUCATION_CHOICES:
            if text.strip() in pair[1]:
                return pair[0]

        return None

    def normalize_rate(self, rate):
        t = float(rate.replace(',', ''))
        print(t)
        return t
