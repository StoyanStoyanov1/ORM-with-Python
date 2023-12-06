from django.db import models


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return self.annotate(num_orders=models.Count('order_profile')).filter(num_orders__gt=2).order_by('-num_orders')

