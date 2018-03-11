from django.contrib import admin
from .models import Activity, Lap, DataPoint

admin.site.register(Activity)
admin.site.register(Lap)
admin.site.register(DataPoint)
