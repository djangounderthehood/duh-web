from django.views import generic

from .models import Entry


class ListView(generic.ListView):
    template_name = 'FAQ/list.html'
    model = Entry

    def get_queryset(self):
        """
        Only show published entries.
        """
        queryset = super(ListView, self).get_queryset()
        queryset = queryset.published()
        return queryset
