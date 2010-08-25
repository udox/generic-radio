from django.db.models import Q, Manager
from datetime import date
from django.conf import settings

class ShowManager(Manager):
    """ A manger for switchable objects ordered by descending created date """
    def get_query_set(self):
        return super(ShowManager, self).get_query_set().filter(status=5).order_by('-created_at')
