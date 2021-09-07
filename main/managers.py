from django.db import models
from django.db.models import Q


class JobQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = (
            Q(name__icontains=query)
        )
        return self.filter(lookups).distinct()


class JobManager(models.Manager):
    def get_queryset(self):
        return JobQuerySet(self.model, using=self.db)

    def search(self, query):
        return self.get_queryset().search(query)