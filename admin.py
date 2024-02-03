from django.contrib import admin

from base.models.customer import Customer
from base.models.useractivity import UserActivity
# Register your models here.
admin.site.register(Customer)
admin.site.register(UserActivity)