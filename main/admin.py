from django.contrib import admin
from .models import Record, Stock, Person

# Register your models here.

admin.site.register(Record)
admin.site.register(Stock)
admin.site.register(Person)