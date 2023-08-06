from django.contrib import admin
from .models import (
    LaundryOutlet,
    PredeterminedServiceCategory,
    ItemCategoryProvided
)


admin.site.register(LaundryOutlet)
admin.site.register(PredeterminedServiceCategory)
admin.site.register(ItemCategoryProvided)
