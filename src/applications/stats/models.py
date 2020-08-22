import datetime
from typing import NamedTuple, Optional

from django.db import models
from delorean import Delorean
# Create your models here.
from django.db.models import Q
from pandas import DataFrame

from utils.utils import asdict


class Value(NamedTuple):
    value: str


class Intervals(NamedTuple):
    m05: Value
    m15: Value
    m60: Value
    h24: Value


class Dashboard(NamedTuple):
    error_rate: Intervals


class Stats(models.Model):
    url = models.URLField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    method = models.TextField(null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    user = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    @classmethod
    def generate_dashboard(cls):
        stats = Stats.objects.all()
        error_code = Q(code__gte=400) & Q(code__lte=599)
        now = datetime.datetime.now()
        params = {}
        dimensions = {"error_rate": "code"}

        for measure_attr, minutes in zip(Intervals.__annotations__, (5, 15, 60, 60 * 24)):
            delta = datetime.timedelta(minutes=minutes)
            time = (now - delta)

            for dimension_attr, dimension in dimensions.items():
                value = stats.filter(Q(date__gte=time) & Q(error_code)).count()

                metric = Value(value=value)
                params.setdefault(dimension_attr, {})[measure_attr] = metric

        dashboard = Dashboard(**params)

        return dashboard
