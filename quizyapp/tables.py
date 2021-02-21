from django_tables2 import tables
from .models import UserPoints

class PersonTable(tables.Table):
    class Meta:
        model = UserPoints
#    points = tables.Column(order_by=("first_name", "family_name"))